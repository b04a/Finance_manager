from flask import Flask, render_template, request, redirect, url_for
from utils import format_date
from models import (
    create_table,
    add_transaction,
    get_transactions,
    calculate_balance,
    delete_transaction,
    update_transaction,
    get_category_stats,
)
import sqlite3

DB_NAME = "finance_manager.db"

app = Flask(__name__)
create_table()

@app.route('/')
def index():
    category_stats = get_category_stats()
    transactions = get_transactions()
    balance = calculate_balance()
    return render_template('index.html', transactions=transactions, balance=balance, category_stats=category_stats, format_date=format_date)

@app.route('/add_transaction', methods=['POST'])
def add_transaction_route():
    try:
        amount = float(request.form['amount'])
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        type = request.form['type']
        category = request.form['category']
        date = request.form['date']

        # Добавляем транзакцию в базу данных
        add_transaction(amount, type, category, date)
        return redirect(url_for('index'))
    except ValueError as e:
        return render_template('index.html', error_message=str(e), transactions=get_transactions(),
                               balance=calculate_balance())


@app.route('/delete_transaction/<int:transaction_id>', methods=['GET'])
def delete_transaction_route(transaction_id):
    delete_transaction(transaction_id)
    return redirect(url_for('index'))


@app.route('/edit_transaction/<int:transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")
            type = request.form['type']
            category = request.form['category']
            date = request.form['date']

            # Обновляем транзакцию в базе данных
            update_transaction(transaction_id, amount, type, category, date)
            return redirect(url_for('index'))
        except ValueError as e:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM transactions WHERE id = ?', (transaction_id,))
            transaction = cursor.fetchone()
            conn.close()
            return render_template('edit_transaction.html', transaction=transaction, error_message=str(e))
    else:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM transactions WHERE id = ?', (transaction_id,))
        transaction = cursor.fetchone()
        conn.close()
        return render_template('edit_transaction.html', transaction=transaction)


if __name__ == '__main__':
    app.run(debug=True)
