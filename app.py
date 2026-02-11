import streamlit as st
import pandas as pd
import os

from database import init_db, add_holding, get_holdings, request_sell

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Holding Hub", layout="centered")

# ---------------- STARTUP ----------------
st.write("App started")

# ---------------- INIT DATABASE ----------------
init_db()

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = None

# ---------------- CONSTANTS ----------------
USERS_FILE = "users.csv"

# ---------------- SIDEBAR: ADMIN SETUP ----------------
st.sidebar.header("⚙️ Admin Setup")

# ---------------- USERS FILE CHECK ----------------
if not os.path.exists(USERS_FILE):
    st.sidebar.warning("users.csv not found. Please upload it to continue.")

    uploaded_users = st.sidebar.file_uploader(
        "Upload users.csv",
        type=["csv"]
    )

    if uploaded_users is not None:
        users_df = pd.read_csv(uploaded_users)
        users_df.to_csv(USERS_FILE, index=False)
        st.sidebar.success("users.csv uploaded successfully. Please refresh the page.")

    st.stop()  # stop AFTER showing upload UI

# ---------------- LOAD USERS ----------------
users_df = pd.read_csv(USERS_FILE)

if "email" not in users_df.columns:
    st.error("❌ users.csv must contain an 'email' column")
    st.stop()

users_df = users_df[users_df["email"].notna()]
users_df["email"] = users_df["email"].astype(str).str.lower()
valid_emails = users_df["email"].tolist()

# ---------------- LOGIN ----------------
st.divider()
st.header("Login")

login_email = st.text_input("Email to login")

if st.button("Login"):
    if login_email.lower() in valid_emails:
        st.session_state.logged_in = True
        st.session_state.user_email = login_email.lower()
        st.success("Logged in successfully")
    else:
        st.error("Email not authorized")

# ---------------- ADMIN SETUP ----------------
st.divider()
st.header("Admin Setup")

admin_email = st.text_input("Admin Email")
admin_password = st.text_input("Password", type="password")

if st.button("Create Admin"):
    if not admin_email or not admin_password:
        st.error("Please enter email and password")
    else:
        st.success("Admin created (placeholder logic)")

# ---------------- DASHBOARD ----------------
if st.session_state.logged_in:
    st.divider()
    st.header("📊 Holdings Dashboard")
    st.write(f"Welcome, {st.session_state.user_email}")

    holdings = get_holdings()

    if holdings is not None and len(holdings) > 0:
        st.dataframe(holdings)
    else:
        st.info("No holdings found yet.")

st.write("✅ App loaded successfully")