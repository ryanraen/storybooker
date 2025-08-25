from flask import Flask, request, jsonify
from services.agent import run
import os
from supabase import create_client, Client
import dotenv

app = Flask(__name__)

dotenv.load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
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
            "id": user_id,
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
    try:
        auth_response = supabase.auth.update_user({"password": new_password})
        if not auth_response.user:
            return jsonify({"error": "Password update failed"}), 400
        
        return jsonify({"message": "Password updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
        
@app.route("/user/logout", methods = ["POST"])
def logout():
    try:
        supabase.auth.sign_out()
        return jsonify({"message": "User logged out"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
  
    
# Agent
@app.route("/generate", methods = ["POST"])
def generate():
    ...