import sqlite3

DB_NAME = "holdings.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS holdings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            symbol TEXT,
            shares_owned INTEGER,
            buy_price REAL,
            current_price REAL
        )
    """)

    conn.commit()
    conn.close()


def add_holding(email, symbol, shares_owned, buy_price, current_price):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Replace existing holding for same user + stock
    c.execute(
        "DELETE FROM holdings WHERE email = ? AND symbol = ?",
        (email, symbol)
    )

    c.execute("""
        INSERT INTO holdings (email, symbol, shares_owned, buy_price, current_price)
        VALUES (?, ?, ?, ?, ?)
    """, (email, symbol, shares_owned, buy_price, current_price))

    conn.commit()
    conn.close()


def get_holdings(email):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        SELECT symbol, shares_owned, buy_price, current_price
        FROM holdings
        WHERE email = ?
    """, (email,))

    rows = c.fetchall()
    conn.close()

    return [
        {
            "symbol": r[0],
            "shares_owned": r[1],
            "buy_price": r[2],
            "current_price": r[3]
        }
        for r in rows
    ]


def request_sell(email, symbol, quantity):
    # For now, just log the request (HF-safe)
    print(f"SELL REQUEST → {email} | {symbol} | {quantity}")