from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import re
import requests
from collections import defaultdict
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app)

# ── Config
VALID_USERNAME = "user"
VALID_PASSWORD = "pass123"
VALID_API_KEY  = "SECURE-KEY-999"

REAL_API_URL      = "http://localhost:5001"
HONEYPOT_API_URL  = "http://localhost:5002"

LOG_PATH = os.path.join(os.path.dirname(__file__), "logs", "honeypot_log.json")

# ── Rate-limit tracking (in-memory)
# { ip: [datetime, datetime, ...] }
request_timestamps = defaultdict(list)

SQL_PATTERNS = re.compile(
    r"('|--|;|\/\*|\*\/|xp_|union\s+select|select\s+.*\s+from|"
    r"insert\s+into|drop\s+table|or\s+1\s*=\s*1|and\s+1\s*=\s*1|"
    r"exec\s*\(|cast\s*\(|convert\s*\()",
    re.IGNORECASE,
)

BAD_USERNAMES = {"admin", "root", "test", "administrator", "superuser", "guest"}

os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

 

def load_logs():
    if not os.path.exists(LOG_PATH):
        return []
    with open(LOG_PATH, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_log(entry: dict):
    logs = load_logs()
    logs.append(entry)
    with open(LOG_PATH, "w") as f:
        json.dump(logs, f, indent=2)


def rate_limited(ip: str) -> bool:
    now = datetime.utcnow()
    window_start = now - timedelta(minutes=1)
    timestamps = request_timestamps[ip]
    # Prune old timestamps
    timestamps = [t for t in timestamps if t > window_start]
    timestamps.append(now)
    request_timestamps[ip] = timestamps
    return len(timestamps) > 5


def contains_sql_injection(text: str) -> bool:
    return bool(SQL_PATTERNS.search(text))


def calculate_score(ip: str, username: str, password: str, api_key: str) -> tuple[int, list]:
    score = 0
    reasons = []

    # Wrong / missing API key
    if api_key != VALID_API_KEY:
        score += 3
        reasons.append("Invalid/missing API key (+3)")

    # Rate limit exceeded
    if rate_limited(ip):
        score += 2
        reasons.append("Rate limit exceeded (+2)")

    # SQL injection in any field
    for field_name, value in [("username", username), ("password", password)]:
        if contains_sql_injection(value):
            score += 5
            reasons.append(f"SQL injection pattern in {field_name} (+5)")
            break 

    # Known bad usernames
    if username.strip().lower() in BAD_USERNAMES:
        score += 2
        reasons.append(f"Known bad username '{username}' (+2)")

    return score, reasons




@app.route("/")
def index():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True, silent=True) or {}

    username = data.get("username", "")
    password = data.get("password", "")
    api_key  = data.get("api_key", "") or request.headers.get("X-API-Key", "")
    ip       = request.remote_addr

    score, reasons = calculate_score(ip, username, password, api_key)

    if score >= 5:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "ip": ip,
            "username": username,
            "password": password,
            "api_key": api_key,
            "score": score,
            "reasons": reasons,
            "routed_to": "honeypot",
        }
        save_log(log_entry)

        try:
            resp = requests.post(
                f"{HONEYPOT_API_URL}/honeypot-login",
                json={"username": username, "password": password},
                timeout=5,
            )
            hp_data = resp.json()
        except Exception:
            hp_data = {"status": "Login successful", "token": "fake-token-xyz"}

        return jsonify({
            "routed_to": "honeypot",
            "score": score,
            "reasons": reasons,
            "response": hp_data,
            "redirect": "/fake-dashboard",
        })

    else:
        # ── Route to real API
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            try:
                resp = requests.post(
                    f"{REAL_API_URL}/real-login",
                    json={"username": username, "password": password},
                    headers={"X-API-Key": api_key},
                    timeout=5,
                )
                real_data = resp.json()
            except Exception:
                real_data = {"status": "Welcome", "data": ["record1", "record2", "record3"]}

            return jsonify({
                "routed_to": "real",
                "score": score,
                "response": real_data,
                "redirect": "/real-dashboard",
            })
        else:
            # Wrong credentials 
            return jsonify({
                "routed_to": "rejected",
                "score": score,
                "error": "Invalid credentials",
            }), 401


@app.route("/real-dashboard")
def real_dashboard():
    return render_template("real_dashboard.html")


@app.route("/fake-dashboard")
def fake_dashboard():
    return render_template("fake_dashboard.html")


@app.route("/monitor")
def monitor():
    return render_template("monitor.html")


@app.route("/logs", methods=["GET"])
def get_logs():
    return jsonify(load_logs())


if __name__ == "__main__":
    print("🔐 API Gateway running on http://localhost:5000")
    app.run(port=5000, debug=True)