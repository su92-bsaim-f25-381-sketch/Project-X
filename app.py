from flask import Flask, jsonify, request, send_file
from bot_engine import ProjectXEngine

app = Flask(__name__)
engine = ProjectXEngine()
custom_balance = 1000.0

@app.route("/")
def home():
    return send_file("index.html")

@app.route("/api/status", methods=["GET"])
def get_status():
    bal = engine.get_account_balance() if engine.mt5_connected else custom_balance
    return jsonify({
        "balance": round(bal, 2),
        "risk_percentage": engine.risk_percentage,
        "stop_loss": engine.stop_loss_pips,
        "take_profit": engine.take_profit_pips,
        "is_active": engine.is_active,
        "total_trades": engine.total_trades,
        "wins": engine.wins,
        "losses": engine.losses,
        "win_rate": engine.win_rate(),
        "trade_history": engine.trade_history[::-1]
    })

@app.route("/api/toggle", methods=["POST"])
def toggle():
    engine.is_active = not engine.is_active
    return jsonify({"success": True, "is_active": engine.is_active})

@app.route("/api/update_balance", methods=["POST"])
def update_balance():
    global custom_balance
    data = request.json
    custom_balance = float(data.get("balance", custom_balance))
    return jsonify({"success": True})

@app.route("/api/update_risk", methods=["POST"])
def update_risk():
    data = request.json
    engine.risk_percentage = float(data.get("risk_percentage", 2.0))
    return jsonify({"success": True})

@app.route("/api/update_sltp", methods=["POST"])
def update_sltp():
    data = request.json
    engine.stop_loss_pips = int(data.get("stop_loss", 20))
    engine.take_profit_pips = int(data.get("take_profit", 40))
    return jsonify({"success": True})

@app.route("/api/tick", methods=["POST"])
def tick():
    if not engine.is_active:
        return jsonify({"thinking": "Bot Paused."})

    signal, thinking = engine.analyze_strategy()
    if signal != "NEUTRAL":
        engine.execute_trade(signal)
    
    return jsonify({"thinking": thinking, "signal": signal})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
