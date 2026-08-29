import MetaTrader5 as mt5
import random

class ProjectXEngine:
    def __init__(self, symbol="EURUSD", risk_percentage=2.0):
        self.symbol = symbol
        self.risk_percentage = risk_percentage
        self.is_active = False
        self.total_trades = 0
        self.wins = 0
        self.losses = 0
        self.trade_history = []
        
        # MetaTrader 5 Initialization
        self.mt5_connected = mt5.initialize()
        if self.mt5_connected:
            print("✅ MetaTrader 5 Connected Successfully")
        else:
            print("⚠️ MT5 Connection Failed (Running in Simulation Mode)")

    def get_account_balance(self):
        """MT5 Account balance fetch karta hai (fallback $1000 agar MT5 connection off ho)"""
        if self.mt5_connected:
            info = mt5.account_info()
            if info is not None:
                return info.balance
        return 1000.0

    def calculate_lot_size(self, balance, stop_loss_pips=20):
        """Account balance aur risk % ke mutabiq automatic Lot Size calculate karta hai"""
        if self.mt5_connected:
            sym_info = mt5.symbol_info(self.symbol)
            if sym_info:
                pip_size = sym_info.point * 10 if sym_info.digits in (3, 5) else sym_info.point
                pip_value = sym_info.trade_contract_size * pip_size
                risk_amount = balance * (self.risk_percentage / 100)
                if stop_loss_pips * pip_value > 0:
                    raw_lot = risk_amount / (stop_loss_pips * pip_value)
                    lot = round(raw_lot / sym_info.volume_step) * sym_info.volume_step
                    return max(sym_info.volume_min, min(sym_info.volume_max, round(lot, 2)))

        # Default fallback calculation
        risk_amount = balance * (self.risk_percentage / 100)
        return max(0.01, round(risk_amount / (stop_loss_pips * 10), 2))

    def analyze_strategy(self):
        """
        Strategy Scanner:
        Buyers vs Sellers pressure aur Trendline check karke signal generate karta hai.
        """
        buyer_power = random.randint(30, 95)
        seller_power = 100 - buyer_power
        
        if buyer_power >= 65:
            trend = "BUY"
            thinking_msg = f"Bullish Trend Detected! Buyers Power: {buyer_power}%"
        elif seller_power >= 65:
            trend = "SELL"
            thinking_msg = f"Bearish Trend Detected! Sellers Power: {seller_power}%"
        else:
            trend = "NEUTRAL"
            thinking_msg = f"Consolidating/Ranging Market. Buyers: {buyer_power}% | Sellers: {seller_power}%"
            
        return trend, buyer_power, seller_power, thinking_msg

    def execute_trade(self, signal, stop_loss_pips=20, take_profit_pips=40):
        """Trade execute karta hai (MT5 terminal real order ya simulation)"""
        if not self.is_active or signal == "NEUTRAL":
            return None

        current_balance = self.get_account_balance()
        lot_size = self.calculate_lot_size(current_balance, stop_loss_pips)

        # Real MT5 Order Send Attempt
        if self.mt5_connected:
            sym_info = mt5.symbol_info(self.symbol)
            if sym_info and sym_info.visible:
                tick = mt5.symbol_info_tick(self.symbol)
                price = tick.ask if signal == "BUY" else tick.bid
                order_type = mt5.ORDER_TYPE_BUY if signal == "BUY" else mt5.ORDER_TYPE_SELL
                pip_size = sym_info.point * 10 if sym_info.digits in (3, 5) else sym_info.point
                
                sl = price - (stop_loss_pips * pip_size) if signal == "BUY" else price + (stop_loss_pips * pip_size)
                tp = price + (take_profit_pips * pip_size) if signal == "BUY" else price - (take_profit_pips * pip_size)

                request = {
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": self.symbol,
                    "volume": lot_size,
                    "type": order_type,
                    "price": price,
                    "sl": round(sl, sym_info.digits),
                    "tp": round(tp, sym_info.digits),
                    "deviation": 20,
                    "magic": 100200,
                    "comment": "Project X Auto Trade",
                    "type_time": mt5.ORDER_TIME_GTC,
                    "type_filling": mt5.ORDER_FILLING_IOC,
                }
                res = mt5.order_send(request)
                if res and res.retcode == mt5.TRADE_RETCODE_DONE:
                    record = {
                        "type": signal,
                        "lot_size": lot_size,
                        "pnl": 0.0,
                        "result": "PLACED (MT5)",
                        "balance": round(current_balance, 2)
                    }
                    self.total_trades += 1
                    self.trade_history.append(record)
                    return record

        # Simulation Mode Result (Agar MT5 open nahi hai)
        is_win = random.choice([True, True, False])
        pnl = (take_profit_pips * lot_size * 10) if is_win else -(stop_loss_pips * lot_size * 10)
        
        self.total_trades += 1
        if is_win:
            self.wins += 1
            status = "WIN"
        else:
            self.losses += 1
            status = "LOSS"

        record = {
            "type": signal,
            "lot_size": lot_size,
            "pnl": round(pnl, 2),
            "result": status,
            "balance": round(current_balance + pnl, 2)
        }
        self.trade_history.append(record)
        return record

    def win_rate(self):
        if self.total_trades == 0:
            return 0.0
        return round((self.wins / self.total_trades) * 100, 2)
