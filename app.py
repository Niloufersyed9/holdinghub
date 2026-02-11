import streamlit as st
import pandas as pd
import os
import yfinance as yf

from database import init_db, add_holding, get_holdings, request_sell

# ================== APP SETUP ==================
st.set_page_config(page_title="Holding Hub", layout="wide")
init_db()

USERS_FILE = "users.csv"

# ================== AUTH ==================
if not os.path.exists(USERS_FILE):
    st.sidebar.error("users.csv not found")
    uploaded = st.sidebar.file_uploader("Upload users.csv", type=["csv"])
    if uploaded:
        pd.read_csv(uploaded).to_csv(USERS_FILE, index=False)
        st.sidebar.success("Uploaded users.csv. Refresh the page.")
    st.stop()

users_df = pd.read_csv(USERS_FILE)
users_df["email"] = users_df["email"].astype(str).str.lower().str.strip()
allowed_emails = users_df["email"].tolist()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "email" not in st.session_state:
    st.session_state.email = None

if not st.session_state.logged_in:
    st.title("🔐 Login")
    email_input = st.text_input("Email")

    if st.button("Login"):
        if email_input.lower().strip() in allowed_emails:
            st.session_state.logged_in = True
            st.session_state.email = email_input.lower().strip()
            st.rerun()
        else:
            st.error("Email not authorized")

    st.stop()

email = st.session_state.email

# ================== HEADER ==================
st.title("📊 Holding Hub")
st.caption(f"Logged in as **{email}**")

st.divider()

# ================== ADD HOLDING ==================
st.subheader("➕ Add Holding")

with st.form("add_holding_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)

    with col1:
        symbol = st.text_input("Stock Symbol (e.g. AAPL)")
    with col2:
        shares = st.number_input("Shares", min_value=1, step=1)
    with col3:
        buy_price = st.number_input("Buy Price", min_value=0.0, step=0.01)

    submitted = st.form_submit_button("Add Holding")

    if submitted:
        if not symbol:
            st.error("Stock symbol is required")
        else:
            add_holding(email, symbol, shares, buy_price)
            st.success("✅ Holding added")
            st.rerun()

# ================== DASHBOARD ==================
st.divider()
st.subheader("📈 Your Holdings")

df = get_holdings(email)

if df.empty:
    st.info("You don’t own any stocks yet. Add one above 👆")
else:
    prices = {}

    for sym in df["symbol"].unique():
        try:
            hist = yf.Ticker(sym).history(period="1d")
            prices[sym] = float(hist["Close"].iloc[-1])
        except Exception:
            prices[sym] = None

    df["Current Price"] = df["symbol"].map(prices)
    df["Buy Value"] = df["shares"] * df["buy_price"]
    df["Current Value"] = df["shares"] * df["Current Price"]
    df["P/L"] = df["Current Value"] - df["Buy Value"]

    st.dataframe(df, use_container_width=True)

# ================== SELL ==================
st.divider()
st.subheader("💸 Sell Shares")

if not df.empty:
    sell_symbol = st.selectbox("Select Stock", df["symbol"].unique())
    owned_shares = int(df[df["symbol"] == sell_symbol]["shares"].sum())

    sell_qty = st.number_input(
        "Shares to sell",
        min_value=1,
        max_value=owned_shares,
        step=1
    )

    if st.button("Request Sell"):
        request_sell(email, sell_symbol, sell_qty)
        st.success("📨 Sell request sent to company")