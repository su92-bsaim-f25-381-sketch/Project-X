import random

class ProjectXEngine:
    def __init__(self, balance=1000.0, risk_percentage=2.0):
        # Account Settings
        self.balance = balance
        self.risk_percentage = risk_percentage
        self.is_active = False
        
        # Stats & Performance Tracking
        self.total_trades = 0
        self.wins = 0
        self.losses = 0
        self.trade_history = []

    def calculate_lot_size(self, stop_loss_pips=20, pip_value_per_lot=10):
        """
        Risk Management System:
        User balance aur risk percentage ke hisaab se automatic Lot Size nikaltay hain.
        """
        risk_amount = self.balance * (self.risk_percentage / 100)
        
        if stop_loss_pips * pip_value_per_lot == 0:
            return 0.01
            
        lot_size = risk_amount / (stop_loss_pips * pip_value_per_lot)
        # Minimum lot size 0.01 set kia hai
        return max(0.01, round(lot_size, 2))

    def analyze_market(self):
        """
        Trend & Strategy Scanner:
        Buyers vs Sellers pressure aur Trendlines check karti hai.
        """
        buyer_power = random.randint(30, 90)
        seller_power = 100 - buyer_power
        
        if buyer_power > 65:
            trend = "BUY"
        elif seller_power > 65:
            trend = "SELL"
        else:
            trend = "NEUTRAL"
            
        return trend, buyer_power, seller_power

    def execute_trade(self, signal, stop_loss_pips=20, take_profit_pips=40):
        """
        Automatic Trade Execution Logic
        """
        if signal == "NEUTRAL" or not self.is_active:
            return None

        lot_size = self.calculate_lot_size(stop_loss_pips)
        
        # Win / Loss Result Simulation (Real deployment par yahan Broker API connect hogi)
        is_win = random.choice([True, True, False])  # Mock probability
        
        if is_win:
            profit_loss = take_profit_pips * lot_size * 10
            self.wins += 1
            status = "WIN"
        else:
            profit_loss = -(stop_loss_pips * lot_size * 10)
            self.losses += 1
            status = "LOSS"

        # Balance update aur stats record
        self.balance += profit_loss
        self.total_trades += 1

        trade_record = {
            "type": signal,
            "lot_size": lot_size,
            "pnl": round(profit_loss, 2),
            "result": status,
            "balance": round(self.balance, 2)
        }
        
        self.trade_history.append(trade_record)
        return trade_record

    def win_rate(self):
        """Win Rate calculate karny ka function"""
        if self.total_trades == 0:
            return 0.0
        return round((self.wins / self.total_trades) * 100, 2)
