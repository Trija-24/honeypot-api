from flask import Flask, request, jsonify
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)


@app.route("/honeypot-login", methods=["POST"])
def honeypot_login():
    # Fake delay to appear like a real processing server
    time.sleep(1.5)

    
    return jsonify({
        "status": "Login successful",
        "token": "fake-token-xyz",
        "message": "Welcome back. Loading your dashboard...",
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "honeypot_running", "port": 5002})


if __name__ == "__main__":
    print("🍯 Honeypot API running on http://localhost:5002")
    app.run(port=5002, debug=True)