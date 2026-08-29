from flask import Flask, jsonify, request, send_file
from bot_engine import MultiSectionEngine

app = Flask(__name__)
engine = MultiSectionEngine()

@app.route("/")
def home():
    return send_file("index.html")

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    
    success, message = engine.login_and_start(email, password)
    return jsonify({"success": success, "message": message})

@app.route("/api/status", methods=["GET"])
def get_status():
    return jsonify({
        "balance": engine.get_account_balance(),
        "is_active": engine.is_active,
        "user_email": engine.user_email,
        "sections": engine.sections,
        "trade_logs": engine.trade_logs[:15]
    })

@app.route("/api/process_sections", methods=["POST"])
def process_sections():
    if engine.is_active:
        engine.process_all_sections()
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
