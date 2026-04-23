import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app) 

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("MONGO_DB")]
collection = db[os.getenv("MONGO_COLLECTION")]

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()

    if not name or not email or not message:
        return jsonify({"error": "All fields are required"}), 400

    try:
        collection.insert_one({
            "name": name,
            "email": email,
            "message": message
        })
        return jsonify({"message": "Data submitted successfully"}), 201

    except PyMongoError as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
