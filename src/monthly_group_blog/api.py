from flask import Flask, request, jsonify
from flask_cors import CORS
from .database_connection import insert_member_to_group, insert_blog_body
from .main import send_email

app = Flask(__name__)
CORS(app, origins=["https://www.dannyhazley.com"])

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

@app.post("/api/groups/members")
def add_member():
    data = request.get_json(force=True)

    insert_member_to_group(data["group_id"], data["member_email"], data["member_name"])

    return jsonify({"message": "Member Added Successfully"}), 201

@app.post("/api/blog-bodies")
def add_blog_body():
    data = request.get_json(force=True)

    insert_blog_body(data["group_id"], data["email"], data["header"], data["body"], data["image"])

    return jsonify({"message": "Blog Body Added Successfully"}), 201

@app.post("/api/send-email")
def trigger_email():
    data = request.get_json(force=True)

    send_email(data["group_id"])

    return jsonify({"message": "Email Sent Successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)