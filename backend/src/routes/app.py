from flask import Flask, request, jsonify
# from services.agent import run
import os
from supabase import create_client, Client
import dotenv

app = Flask(__name__)

dotenv.load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
db = create_client(url, key)

# user should be able to:
# generate storybook
# preview storybook without downloading
# download storybook
# retrieve past storybooks (history)
# delete history 

auth_response = db.auth.sign_in_with_password({
    "email": os.environ.get("SUPABASE_DUMMY_ACCOUNT_EMAIL"),
    "password": os.environ.get("SUPABASE_DUMMY_ACCOUNT_PASSWORD")
})
# print("Auth response:", auth_response)

session = auth_response.session
access_token = session.access_token
# print("Access token:", access_token)

test_storybook = {
    "user_id": auth_response.user.id,  # matches auth.uid()
    "title": "Dragon Learns Kindness",
    "prompt": "A dragon learns kindness",
    "metadata": {"theme": "kindness", "age_range": "6-8"},
    "pdf_url": "https://example.com/story.pdf"
}

# response = db.table("storybooks").insert(test_storybook).execute()
# print("Insert response:", response)

response = db.table("storybooks").select("*").execute()
print("Storybooks:", response.data)

db.table("storybooks").delete().eq("title", "Dragon Learns Kindness").execute()

print("\n\nDeleted test storybook.\n\n")

response = db.table("storybooks").select("*").execute()
print("Storybooks:", response.data)


# User
# @app.route("/get_users", methods = ["POST"])
# def get_users():


# # Agent
# @app.route("/generate", methods = ["POST"])
# def generate():
#     ...