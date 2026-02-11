import sqlite3
import pandas as pd
import os

# FORCE DB TO LIVE INSIDE STREAMLIT WORKSPACE
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "holdings.db")

def get_conn():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS holdings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            symbol TEXT NOT NULL,
            shares INTEGER NOT NULL,
            buy_price REAL NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS sell_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            symbol TEXT NOT NULL,
            shares INTEGER NOT NULL,
            status TEXT DEFAULT 'PENDING'
        )
    """)

    conn.commit()
    conn.close()

def add_holding(email, symbol, shares, buy_price):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO holdings (email, symbol, shares, buy_price) VALUES (?, ?, ?, ?)",
        (email, symbol.upper(), int(shares), float(buy_price))
    )

    conn.commit()
    conn.close()

def get_holdings(email):
    conn = get_conn()
    df = pd.read_sql(
        "SELECT symbol, shares, buy_price FROM holdings WHERE email = ?",
        conn,
        params=(email,)
    )
    conn.close()
    return df

def request_sell(email, symbol, shares):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO sell_requests (email, symbol, shares) VALUES (?, ?, ?)",
        (email, symbol.upper(), int(shares))
    )

    conn.commit()
    conn.close()