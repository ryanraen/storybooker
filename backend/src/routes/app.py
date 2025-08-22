from flask import Flask, request, jsonify
from services.agent import run

app = Flask(__name__)

# user should be able to:
# generate storybook
# preview storybook without downloading
# download storybook
# retrieve past storybooks (history)
# delete history 

# User
@app.route("/get_users", methods = ["POST"])
def get_users():
    ...

# Agent
@app.route("/generate", methods = ["POST"])
def generate():
    ...