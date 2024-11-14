import sqlite3

DB_NAME = "finance_manager.db"

def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            type TEXT,
            category TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_transaction(amount, type, category, date):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (amount, type, category, date)
        VALUES (?, ?, ?, ?)
    ''', (amount, type, category, date))
    conn.commit()
    conn.close()