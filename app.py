import streamlit as st
import pandas as pd
import os
from database import init_db, add_holding, get_holdings, request_sell

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Holding Hub", layout="centered")

# ---------------- INIT DB ----------------
init_db()

# ---------------- LOAD USERS (SAFE) ----------------
USERS_FILE = "users.csv"

st.sidebar.header("⚙️ Admin Setup")

if not os.path.exists(USERS_FILE):
    st.sidebar.warning("users.csv not found. Please upload it.")

    uploaded_users = st.sidebar.file_uploader(
        "Upload users.csv",
        type=["csv"]
    )

    if uploaded_users:
        users_df = pd.read_csv(uploaded_users)
        users_df.to_csv(USERS_FILE, index=False)
        st.sidebar.success("users.csv uploaded. Refresh the page.")
        st.stop()
    else:
        st.stop()

# If file exists, load it
users_df = pd.read_csv(USERS_FILE)

# Validate email column
if "email" not in users_df.columns:
    st.error("❌ users.csv must contain an 'email' column")
    st.stop()

users_df = users_df[users_df["email"].notna()]
users_df["email"] = users_df["email"].astype(str).str.lower()
valid_emails = users_df["email"].tolist()

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = None