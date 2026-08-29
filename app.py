import streamlit as st
import time
from bot_engine import ProjectXEngine

# Page Layout Configuration
st.set_page_config(
    page_title="Project X - Trading Bot",
    page_icon="🤖",
    layout="wide"
)

# Engine Initialization (Session State maintains state across UI updates)
if "bot" not in st.session_state:
    st.session_state.bot = ProjectXEngine()

bot = st.session_state.bot

st.title("🤖 Project X - Automated Trading Bot Control Center")
st.markdown("---")

# Top Control Panel (Balance, Risk & ON/OFF Switch)
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.subheader("⚙️ Account Settings")
    custom_balance = st.number_input(
        "Set Custom Balance ($):", 
        min_value=10.0, 
        value=float(bot.balance), 
        step=50.0
    )
    if st.button("Update Balance"):
        bot.balance = custom_balance
        st.success(f"Balance updated to ${bot.balance:.2f}")

with col2:
    st.subheader("🛡️ Risk Management")
    bot.risk_percentage = st.slider(
        "Risk Per Trade (%)", 
        min_value=0.5, 
        max_value=10.0, 
        value=float(bot.risk_percentage), 
        step=0.5
    )
    st.info(f"Lot size will be auto-calculated using {bot.risk_percentage}% risk.")

with col3:
    st.subheader("⚡ Bot Status")
    if bot.is_active:
        st.success("STATUS: ONLINE & SCANNING")
        if st.button("🔴 STOP BOT", use_container_width=True):
            bot.is_active = False
            st.rerun()
    else:
        st.error("STATUS: OFFLINE / PAUSED")
        if st.button("🟢 START BOT", use_container_width=True):
            bot.is_active = True
            st.rerun()

st.markdown("---")

# Performance Analytics Cards
st.subheader("📊 Live Performance & Win/Loss Ratio")
m1, m2, m3, m4, m5 = st.columns(5)

m1.metric("Current Balance", f"${bot.balance:.2f}")
m2.metric("Total Trades", bot.total_trades)
m3.metric("Wins 🟢", bot.wins)
m4.metric("Losses 🔴", bot.losses)
m5.metric("Win Rate", f"{bot.win_rate()}%")

st.markdown("---")

# Market Scanner & Execution Section
st.subheader("🔍 Market Trend Scanner & Trade Execution")

if bot.is_active:
    st.info("Bot active hai aur market scan kar raha hai...")
    
    signal, buyers, sellers = bot.analyze_market()
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.write(f"**Buyer Pressure:** {buyers}%")
        st.progress(buyers / 100)
    with col_b:
        st.write(f"**Seller Pressure:** {sellers}%")
        st.progress(sellers / 100)
        
    st.write(f"**Detected Strategy Signal:** `{signal}`")
    
    if signal != "NEUTRAL":
        trade = bot.execute_trade(signal)
        if trade:
            if trade['result'] == 'WIN':
                st.success(f"✅ Trade Closed in PROFIT! Type: **{trade['type']}** | Lot Size: **{trade['lot_size']}** | PnL: **+${trade['pnl']}**")
            else:
                st.error(f"❌ Trade Hit STOP LOSS. Type: **{trade['type']}** | Lot Size: **{trade['lot_size']}** | PnL: **${trade['pnl']}**")
else:
    st.warning("Bot is currently OFF. Press **🟢 START BOT** to trigger automated market scanning and trading.")

st.markdown("---")

# Recent Trade History Table
if bot.trade_history:
    st.subheader("📜 Recent Trade Logs")
    st.dataframe(bot.trade_history[::-1], use_container_width=True)
