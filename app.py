import streamlit as st
import pandas as pd
import os

from database import init_db, add_holding, get_holdings, request_sell

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Holding Hub", layout="centered")

# ---------------- STARTUP ----------------
st.write("App started")

# ---------------- INIT DB ----------------
init_db()

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = None

# ---------------- CONSTANTS ----------------
USERS_FILE = "users.csv"

# ---------------- SIDEBAR: USERS SETUP ----------------
st.sidebar.header("⚙️ Users Setup")

if not os.path.exists(USERS_FILE):
    st.sidebar.warning("users.csv not found. Upload to continue.")

    uploaded = st.sidebar.file_uploader("Upload users.csv", type=["csv"])

    if uploaded is not None:
        df = pd.read_csv(uploaded)
        df.to_csv(USERS_FILE, index=False)
        st.sidebar.success("Uploaded users.csv. Refresh the page.")

    st.stop()

# ---------------- LOAD USERS ----------------
users_df = pd.read_csv(USERS_FILE)

if "email" not in users_df.columns:
    st.error("users.csv must contain a column named 'email'")
    st.stop()

users_df["email"] = users_df["email"].astype(str).str.lower().str.strip()
valid_emails = users_df["email"].tolist()

# 🔎 TEMP DEBUG — REMOVE LATER
st.write("Allowed emails:", valid_emails)

# ---------------- LOGIN ----------------
st.divider()
st.header("Login")

login_email = st.text_input("Email")

if st.button("Login"):
    if login_email.lower().strip() in valid_emails:
        st.session_state.logged_in = True
        st.session_state.user_email = login_email.lower().strip()
        st.success("Logged in successfully")
    else:
        st.error("Email not authorized")

# ---------------- DASHBOARD ----------------
if st.session_state.logged_in:
    st.divider()
    st.header("📊 Holdings Dashboard")
    st.write(f"Welcome, {st.session_state.user_email}")

    holdings = get_holdings(st.session_state.user_email)

    if holdings is not None and len(holdings) > 0:
        st.dataframe(holdings)
    else:
        st.info("No holdings found yet.")

st.write("✅ App loaded successfully")