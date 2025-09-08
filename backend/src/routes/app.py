from flask import Flask, request, jsonify
from flask_cors import CORS
from services.agent import run
import os
from supabase import create_client, Client
import dotenv
import tempfile
from PIL import Image

app = Flask(__name__)
CORS(app)

dotenv.load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SECRET_KEY")
supabase = create_client(url, key)

# user should be able to:
# sign up 
# log in
# reset password
# log out
# update profile (email, password, etc.)
# generate storybook
# preview storybook without downloading
# download storybook
# retrieve past storybooks (history)
# delete history 

# User
@app.route("/user/signup", methods = ["POST"])
def signup():
    data = request.json
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    try:
        auth_response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            })
        user_id = auth_response.user.id
        supabase.table("profiles").insert({
            "user_id": user_id,
            "username": username
            }).execute()
        return jsonify({"message": "User created", "user": user_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route("/user/login", methods = ["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    try:
        auth_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        if not auth_response.user:
            return jsonify({"error": "Invalid credentials"}), 401
        
        return jsonify({
            "user": {
                "id": auth_response.user.id,
                "email": auth_response.user.email,
            },
            "session": {
                "access_token": auth_response.session.access_token,
                "refresh_token": auth_response.session.refresh_token
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route("/user/reset_password", methods = ["POST"])
def reset_password():
    data = request.json
    email = data.get("email")
    redirect_to = data.get("redirect_to") # password reset page
    user, error = get_current_user()
    if error:
        return error
    if user.email != email:
        return jsonify({"error": "Email does not match the logged-in user"}), 403
    try:
        supabase.auth.reset_password_email(
            email,
            {"redirect_to": redirect_to}
        )
        return jsonify({"message": "Password reset email sent"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@app.route("/user/update_password", methods = ["POST"])
def update_password():
    data = request.json
    new_password = data.get("new_password")
    access_token = request.args.get("access_token")
    refresh_token = request.args.get("refresh_token")
    temp_session_response = supabase.auth.set_session({
        "access_token": access_token,
        "refresh_token": refresh_token
    })
    if not temp_session_response.user:
        return jsonify({"error": "Invalid or expired session tokens"}), 401
    try:
        auth_response = supabase.auth.update_user({"password": new_password})
        if not auth_response.user:
            return jsonify({"error": "Password update failed"}), 400
        
        return jsonify({"message": "Password updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
        
@app.route("/user/logout", methods = ["POST"])
def logout():
    user, error = get_current_user()
    if error:
        return error
    try:
        supabase.auth.sign_out()
        return jsonify({"message": "User logged out"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# auth helper
def get_current_user():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None, (jsonify({"error": "Missing or invalid authorization token"}), 401)
    
    token = auth_header.split(" ")[1]  # "Bearer <jwt token>"
    try:
        user = supabase.auth.get_user(token).user
        if not user:
            return None, (jsonify({"error": "Invalid or expired authorization token"}), 401)
        
        return user, None
    except Exception as e:
        return None, (jsonify({"error": str(e)}), 401)
    

def fake_run(prompt: str, temp_dir: str) -> bytes: # for testing without calling LLM services
    in_dir = "/home/ryanraen/storybooker/backend/res/pages/"
    pages = [Image.open(f"{in_dir}scene_{index}.png") for index in range(1, 7)]
    with tempfile.NamedTemporaryFile(mode="wb", dir=temp_dir) as temp_pdf:        
        pages[0].save(
            temp_pdf.name, "PDF" ,resolution=100.0, save_all=True, append_images=pages[1:]
        )
        return open(temp_pdf.name, "rb").read()
    
# Agent
@app.route("/generate", methods = ["POST"])
def generate():
    user, error = get_current_user()
    if error:
        return error
    
    data = request.json
    title = data.get("title")
    prompt = data.get("prompt")
    
    # plan = supabase.table("profiles").("user_id", user.id).select("subscription_tier").execute().data[0]
    profile = supabase.table("profiles").select("*").eq("user_id", user.id).maybe_single().execute().data
    if not profile:
        return jsonify({"error": "User profile not found"}), 404
    remaining_gens = profile.get("remaining_gens")
    if remaining_gens is None or remaining_gens <= 0:
        return jsonify({"error": "No remaining storybook generations. Please upgrade your plan."}), 403
    
    # decrement remaining_gens
    supabase.table("profiles").update({"remaining_gens": remaining_gens - 1}).eq("user_id", user.id).execute()
    
    # run agent
    pdf_bytes = run(prompt)
    if not pdf_bytes:
        return jsonify({"error": "Storybook generation failed"}), 500
    
    filename = title[:50].replace(" ", "_") + ".pdf"
    upload_url = (
        supabase.storage.from_("storybook_pdfs").create_signed_upload_url(user.id + "/" + filename) # TODO could be security concern; replace signed upload url with diff method 
    )
    response = (
        supabase.storage
        .from_("storybook_pdfs")
        .upload_to_signed_url(
            path=user.id + "/" + filename,
            token=upload_url["token"],
            file=pdf_bytes,
        )
    )
    return jsonify({"message": "Storybook generated successfully"}), 200