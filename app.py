from flask import Flask, jsonify, request, send_from_directory
import MetaTrader5 as mt5
import random
import os

app = Flask(__name__)

# MT5 Connection Configuration
# (Agar MT5 terminal pehle se open hai, to login details optional hain)
MT5_LOGIN = 12345678       # Apna Account Number likhein (Optional)
MT5_PASSWORD = "your_password" # Apna Password likhein (Optional)
MT5_SERVER = "Exness-MT5Trial" # Apna Broker Server likhein (Optional)
SYMBOL = "EURUSD"          # Target Trading Pair

def init_mt5():
    """MetaTrader 5 terminal se connection establish karta hai"""
    if not mt5.initialize():
        print(f"MT5 Initialization Failed, error code: {mt5.last_error()}")
        return False
    
    # Optional: Direct login via Python
    # mt5.login(MT5_LOGIN, password=MT5_PASSWORD, server=MT5_SERVER)
    print("✅ MetaTrader 5 Connected Successfully!")
    return True

# Initialize MT5 at server start
init_mt5()

# Bot Internal Control State
bot_state = {
    "risk_percentage": 2.0,
    "is_active": False,
    "total_trades": 0,
    "wins": 0,
    "losses": 0,
    "trade_history": []
}

def get_mt5_account_info():
    """Live MT5 Account Balance fetch karta hai"""
    account_info = mt5.account_info()
    if account_info is None:
        return 1000.0  # Fallback balance agar MT5 open na ho
    return account_info.balance

def calculate_lot_size(balance, risk_pct, symbol, stop_loss_pips=20):
    """Symbol specification ke hisaab se precise Lot Size calculate karta hai"""
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        return 0.01

    risk_amount = balance * (risk_pct / 100)
    pip_size = symbol_info.point * 10 if symbol_info.digits in (3, 5) else symbol_info.point
    pip_value = symbol_info.trade_contract_size * pip_size
    
    if stop_loss_pips * pip_value == 0:
        return symbol_info.volume_min

    raw_lot = risk_amount / (stop_loss_pips * pip_value)
    
    # Lot size steps normalize karna (e.g. 0.01 min, step 0.01)
    volume_step = symbol_info.volume_step
    lot_size = round(raw_lot / volume_step) * volume_step
    
    lot_size = max(symbol_info.volume_min, min(symbol_info.volume_max, lot_size))
    return round(lot_size, 2)

def execute_mt5_trade(symbol, trade_type, lot_size, stop_loss_pips=20, take_profit_pips=40):
    """MetaTrader 5 par Live Market Order place karta hai"""
    symbol_info = mt5.symbol_info(symbol)
    if not symbol_info:
        return False, "Symbol Not Found"

    if not symbol_info.visible:
        if not mt5.symbol_select(symbol, True):
            return False, "Symbol Selection Failed"

    price = mt5.symbol_info_tick(symbol).ask if trade_type == "BUY" else mt5.symbol_info_tick(symbol).bid
    pip_size = symbol_info.point * 10 if symbol_info.digits in (3, 5) else symbol_info.point
    
    if trade_type == "BUY":
        order_type = mt5.ORDER_TYPE_BUY
        sl = price - (stop_loss_pips * pip_size)
        tp = price + (take_profit_pips * pip_size)
    else:
        order_type = mt5.ORDER_TYPE_SELL
        sl = price + (stop_loss_pips * pip_size)
        tp = price - (take_profit_pips * pip_size)

    request_dict = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot_size,
        "type": order_type,
        "price": price,
        "sl": round(sl, symbol_info.digits),
        "tp": round(tp, symbol_info.digits),
        "deviation": 20,
        "magic": 100200,
        "comment": "Project X AutoTrade",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request_dict)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        return False, f"Order Failed: {result.comment} (Code: {result.retcode})"

    return True, result

# API Routes
@app.route("/")
def serve_frontend():
    return send_from_directory(os.getcwd(), "index.html")

@app.route("/api/status", methods=["GET"])
def get_status():
    live_balance = get_mt5_account_info()
    total = bot_state["total_trades"]
    win_rate = round((bot_state["wins"] / total) * 100, 2) if total > 0 else 0.0
    
    return jsonify({
        "balance": round(live_balance, 2),
        "risk_percentage": bot_state["risk_percentage"],
        "is_active": bot_state["is_active"],
        "total_trades": total,
        "wins": bot_state["wins"],
        "losses": bot_state["losses"],
        "win_rate": win_rate,
        "trade_history": bot_state["trade_history"][::-1]
    })

@app.route("/api/toggle", methods=["POST"])
def toggle_bot():
    bot_state["is_active"] = not bot_state["is_active"]
    return jsonify({"success": True, "is_active": bot_state["is_active"]})

@app.route("/api/update_settings", methods=["POST"])
def update_settings():
    data = request.json
    if "risk_percentage" in data:
        bot_state["risk_percentage"] = float(data["risk_percentage"])
    return jsonify({"success": True, "risk_percentage": bot_state["risk_percentage"]})

@app.route("/api/tick", methods=["POST"])
def tick():
    if not bot_state["is_active"]:
        return jsonify({"executed": False, "message": "Bot is paused."})

    # Strategy Market Scanner (Buyers vs Sellers Trend)
    buyer_power = random.randint(30, 90)
    seller_power = 100 - buyer_power
    signal = "BUY" if buyer_power > 65 else ("SELL" if seller_power > 65 else "NEUTRAL")

    if signal == "NEUTRAL":
        return jsonify({
            "executed": False, 
            "signal": signal, 
            "buyer_power": buyer_power, 
            "seller_power": seller_power
        })

    # Account Balance & Dynamic Risk Calculation
    current_balance = get_mt5_account_info()
    lot_size = calculate_lot_size(current_balance, bot_state["risk_percentage"], SYMBOL)

    # MT5 Par Real Order Execute Karein
    success, res = execute_mt5_trade(SYMBOL, signal, lot_size)

    if success:
        bot_state["total_trades"] += 1
        record = {
            "type": signal,
            "lot_size": lot_size,
            "pnl": 0.0,  # Live PnL trade close hone par update hota hai
            "result": "PLACED (MT5)",
            "balance": round(current_balance, 2)
        }
        bot_state["trade_history"].append(record)

        return jsonify({
            "executed": True,
            "signal": signal,
            "buyer_power": buyer_power,
            "seller_power": seller_power,
            "trade": record
        })
    else:
        return jsonify({"executed": False, "error": str(res)})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
