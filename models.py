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

def get_transactions():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions ORDER BY amount DESC')
    transactions = cursor.fetchall()
    return transactions


def calculate_balance():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT type, amount FROM transactions')
    transactions = cursor.fetchall()

    income = sum(amount for t_type, amount in transactions if t_type == 'income')
    expense = sum(amount for t_type, amount in transactions if t_type == 'expense')

    balance = income - expense

    return balance


def delete_transaction(transaction_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
    conn.commit()
    conn.close()

def update_transaction(transaction_id, amount, type, category, date):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE transactions
        SET amount = ?, type = ?, category = ?, date = ?
        WHERE id = ?
    ''', (amount, type, category, date, transaction_id))
    conn.commit()
    conn.close()

def get_category_stats():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT category, SUM(amount) FROM transactions WHERE type = "expense" GROUP BY category')
    stats = cursor.fetchall()
    conn.close()
    return stats

















