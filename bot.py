from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

paper_account = {
    "balance": 10000.0,
    "starting_balance": 10000.0,
    "risk_percent": 1.0,
    "daily_risk_percent": 3.0,
    "risk_reward": 2.0,
    "bot_on": False,
    "wins": 0,
    "losses": 0,
    "trades": []
}


@app.route("/")
def home():
    return jsonify({
        "project": "PROJECT X",
        "status": "online",
        "mode": "paper-trading"
    })


@app.route("/account")
def account():

    total = (
        paper_account["wins"]
        + paper_account["losses"]
    )

    win_rate = (
        paper_account["wins"] / total * 100
        if total else 0
    )

    return jsonify({
        "balance": paper_account["balance"],
        "starting_balance":
            paper_account["starting_balance"],
        "wins": paper_account["wins"],
        "losses": paper_account["losses"],
        "win_rate": round(win_rate, 2),
        "trades": paper_account["trades"]
    })


@app.route("/settings", methods=["POST"])
def settings():

    data = request.get_json() or {}

    if "balance" in data:
        value = float(data["balance"])

        if value <= 0:
            return jsonify({
                "error": "Invalid balance"
            }), 400

        paper_account["balance"] = value
        paper_account["starting_balance"] = value

    if "risk_percent" in data:
        paper_account["risk_percent"] = float(
            data["risk_percent"]
        )

    if "daily_risk_percent" in data:
        paper_account["daily_risk_percent"] = float(
            data["daily_risk_percent"]
        )

    if "risk_reward" in data:
        paper_account["risk_reward"] = float(
            data["risk_reward"]
        )

    return jsonify({
        "message": "Settings updated",
        "account": paper_account
    })


@app.route("/bot", methods=["POST"])
def bot():

    data = request.get_json() or {}

    paper_account["bot_on"] = bool(
        data.get("on", False)
    )

    return jsonify({
        "bot_on": paper_account["bot_on"]
    })


@app.route("/paper-trade", methods=["POST"])
def paper_trade():

    data = request.get_json() or {}

    side = data.get("side")

    if side not in ["BUY", "SELL"]:
        return jsonify({
            "error": "Side must be BUY or SELL"
        }), 400

    price = float(data.get("price", 0))

    if price <= 0:
        return jsonify({
            "error": "Valid price required"
        }), 400

    risk_amount = (
        paper_account["balance"]
        * paper_account["risk_percent"]
        / 100
    )

    trade = {
        "side": side,
        "price": price,
        "risk": round(risk_amount, 2),
        "time":
            datetime.utcnow().isoformat()
    }

    paper_account["trades"].append(trade)

    return jsonify({
        "message": "Paper trade recorded",
        "trade": trade
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )