import streamlit as st
import pandas as pd
import os

from database import init_db, add_holding, get_holdings, request_sell

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Holding Hub", layout="centered")

# ---------------- STARTUP DEBUG ----------------
st.write("App started")

# ---------------- INIT DATABASE ----------------
init_db()

# ---------------- CONSTANTS ----------------
USERS_FILE = "users.csv"

# ---------------- SIDEBAR: ADMIN SETUP ----------------
st.sidebar.header("⚙️ Admin Setup")

# If users.csv does NOT exist, ask to upload and stop safely
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

    # Stop AFTER showing UI (prevents blank screen)
    st.stop()

# ---------------- MAIN PAGE: ADMIN SETUP ----------------
st.header("Admin Setup")

# Load users.csv
users_df = pd.read_csv(USERS_FILE)

# Validate required column
if "email" not in users_df.columns:
    st.error("❌ users.csv must contain an 'email' column")
    st.stop()

# Clean emails
users_df = users_df[users_df["email"].notna()]
users_df["email"] = users_df["email"].astype(str).str.lower()
valid_emails = users_df["email"].tolist()

# ---------------- ADMIN CREATION UI ----------------
admin_email = st.text_input("Admin Email")
admin_password = st.text_input("Password", type="password")

if st.button("Create Admin"):
    if not admin_email or not admin_password:
        st.error("Please enter email and password")
    else:
        st.success("Admin created (placeholder logic)")

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = None

st.write("✅ App loaded successfully")