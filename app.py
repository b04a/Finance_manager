from flask import Flask, render_template, request, redirect, url_for
from models import (
    create_table,
    add_transaction,
    get_transactions,
    calculate_balance,
    delete_transaction,
    update_transaction,
)
import sqlite3

DB_NAME = "finance_manager.db"

app = Flask(__name__)
create_table()

@app.route('/')
def index():
    transactions = get_transactions()
    balance = calculate_balance()
    return render_template('index.html', transactions=transactions, balance=balance)

@app.route('/add_transaction', methods=['POST'])
def add_transaction_route():
    amount = float(request.form['amount'])
    type = request.form['type']
    category = request.form['category']
    date = request.form['date']

    add_transaction(amount, type, category, date)
    return redirect(url_for('index'))

@app.route('/delete_transaction/<int:transaction_id>', methods=['GET'])
def delete_transaction_route(transaction_id):
    delete_transaction(transaction_id)
    return redirect(url_for('index'))

@app.route('/edit_transaction/<int:transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions WHERE id = ?', (transaction_id,))
    transaction = cursor.fetchone()
    conn.close()

    if request.method == 'POST':
        amount = float(request.form['amount'])
        type = request.form['type']
        category = request.form['category']
        date = request.form['date']
        update_transaction(transaction_id, amount, type, category, date)
        return redirect(url_for('index'))

    return render_template('edit_transaction.html', transaction=transaction)



if __name__ == '__main__':
    app.run(debug=True)
