from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

VALID_USERNAME = "user"
VALID_PASSWORD = "pass123"


@app.route("/real-login", methods=["POST"])
def real_login():
    data = request.get_json(force=True, silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")

    if username == VALID_USERNAME and password == VALID_PASSWORD:
        return jsonify({
            "status": "Welcome",
            "data": ["record1", "record2", "record3"],
            "user": username,
            "message": "Authenticated successfully. Returning real data.",
        })

    return jsonify({"status": "Unauthorized", "message": "Bad credentials"}), 401


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "real_api_running", "port": 5001})


if __name__ == "__main__":
    print("✅ Real API running on http://localhost:5001")
    app.run(port=5001, debug=True)