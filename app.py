from flask import Flask, render_template, request, redirect, url_for
from models import create_table, add_transaction, get_transactions, calculate_balance

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

if __name__ == '__main__':
    app.run(debug=True)
