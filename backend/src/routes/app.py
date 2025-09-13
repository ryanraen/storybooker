from flask import Flask, Response, json, request, jsonify
from flask_cors import CORS
from ..services.agent import run
import os
from supabase import create_client, Client
import dotenv
import tempfile
from PIL import Image
from base64 import b64encode


def create_app():
    app = Flask(__name__)
    CORS(app, origins=["https://storybooker.vercel.app", "http://localhost:5173"])

    dotenv.load_dotenv()

    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SECRET_KEY")
    supabase = create_client(url, key)

    # TODO user should be able to:
    # update profile (email, password, etc.)
    # preview storybook without downloading

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
        
    @app.route("/user/forgot-password", methods = ["POST"])
    def forgot_password():
        data = request.json
        email = data.get("email")
        reset_page = data.get("reset_page") # password reset page
        try:
            supabase.auth.reset_password_email(
                email
            )
            return jsonify({"message": "Password reset email sent"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @app.route("/user/verify-otp", methods = ["POST"])
    def verify_otp():
        data = request.json
        email = data.get("email")
        otp = data.get("otp")
        password = data.get("password")
        try:
            auth_response = supabase.auth.verify_otp({
                "email": email,
                "token": otp,
                "type": "email"
            })
            if not auth_response.user:
                return jsonify({"error": "OTP verification failed"}), 400
            
            update_response = supabase.auth.update_user({"password": password})
            if not update_response.user:
                return jsonify({"error": "Password update failed"}), 400
            
            return jsonify({"message": "OTP verified and password set successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400
            
    @app.route("/user/logout", methods = ["POST"])
    def logout():
        try:
            supabase.auth.sign_out()
            return jsonify({"message": "User logged out"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    # auth helper
    def get_current_user(access_token: str = None):
        if not access_token:
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return None, (jsonify({"error": "Missing or invalid authorization token"}), 401)
            
            access_token = auth_header.split(" ")[1]  # "Bearer <jwt token>"
            
        try:
            user = supabase.auth.get_user(access_token).user
            if not user:
                return None, (jsonify({"error": "Invalid or expired authorization token"}), 401)
            
            return user, None
        except Exception as e:
            return None, (jsonify({"error": str(e)}), 401)
        
    @app.route("/generate", methods = ["POST"])
    def generate():
        user, error = get_current_user()
        if not user or error:
            return error
        
        data = request.json
        title = data.get("title")
        prompt = data.get("prompt")
        
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
        upload_response = (
            supabase.storage
            .from_("storybook_pdfs")
            .upload_to_signed_url(
                path=user.id + "/" + filename,
                token=upload_url["token"],
                file=pdf_bytes,
            )
        )
        
        supabase.table("storybooks").insert({
            "user_id": user.id,
            "title": title,
            "prompt": prompt,
            "pdf_path": user.id + "/" + filename
        }).execute()
        
        return jsonify({"message": "Storybook generated successfully", "pdf_data": b64encode(pdf_bytes).decode("utf-8")}), 200
        
    @app.route("/get-history", methods = ["GET"])
    def get_history():
        user, error = get_current_user()
        if not user or error:
            return error
        
        try:
            storybooks = supabase.table("storybooks").select("id, title, created_at").eq("user_id", user.id).order("created_at", desc=True).execute().data
            history = [{"id": book["id"], 
                        "title": book["title"], 
                        "date": book["created_at"]} 
                    for book in storybooks]
            return jsonify({"history": history}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        
    @app.route("/book/download", methods = ["GET"])
    def download():
        access_token = request.args.get("access_token")
        user, error = get_current_user(access_token)
        if not user or error:
            return error
        
        storybook_id = request.args.get("storybook_id")
        print(storybook_id)
        if not storybook_id:
            return jsonify({"error": "Missing storybook ID"}), 400
        try:
            storybook_data = supabase.table("storybooks").select("*").eq("id", storybook_id).eq("user_id", user.id).maybe_single().execute().data
            if not storybook_data:
                return jsonify({"error": "Storybook not found"}), 404
            
            pdf_data = supabase.storage.from_("storybook_pdfs").download(storybook_data["pdf_path"])

            filename = storybook_data["title"][:50].replace(" ", "_") + ".pdf"
            return Response(
                pdf_data,
                mimetype="application/pdf",
                headers={
                    "Content-Disposition": f"attachment; filename={filename}"
                }
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        
    @app.route("/book/delete", methods = ["DELETE"])
    def delete():
        access_token = request.args.get("access_token")
        user, error = get_current_user(access_token)
        if not user or error:
            return error
        
        storybook_id = request.args.get("storybook_id")
        print(storybook_id)
        if not storybook_id:
            return jsonify({"error": "Missing storybook ID"}), 400
        try:
            storybook_data = supabase.table("storybooks").select("*").eq("id", storybook_id).eq("user_id", user.id).maybe_single().execute().data
            if not storybook_data:
                return jsonify({"error": "Storybook not found"}), 404
            
            table_delete_response = supabase.table("storybooks").delete().eq("id", storybook_id).eq("user_id", user.id).execute()
            if not table_delete_response:
                return jsonify({"error": "Could not delete storybook from database"}), 400
            
            storage_delete_response = supabase.storage.from_("storybook_pdfs").remove([storybook_data["pdf_path"]])
            if not storage_delete_response:
                return jsonify({"error": "Could not delete storybook from storage"}), 400
            
            return jsonify({"message": "Storybook deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        
    return app