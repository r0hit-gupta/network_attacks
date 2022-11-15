import sqlite3, os, sys
from flask import Flask, render_template, request, g
from flask_cors import CORS

ACCOUNT_NO = sys.argv[1]
USER_NAME = sys.argv[2]
PORT = int(sys.argv[3])

app = Flask(__name__)
app.database = "database.db"
CORS(app)


# Inject user balance so that it can be used in base.html
@app.context_processor
def inject_balance():
    g.db = get_db()
    query = g.db.execute(
        "SELECT SUM(amount) FROM transactions WHERE receiver=?", [ACCOUNT_NO])
    balance = query.fetchone()[0]
    query = g.db.execute("SELECT SUM(amount) FROM transactions WHERE sender=?",
                         [ACCOUNT_NO])
    sent = query.fetchone()[0]
    balance -= sent if sent else 0
    g.db.close()
    return dict(
        balance=balance,
        account_no=ACCOUNT_NO,
        user_name=USER_NAME,
    )


@app.route('/')
def index():
    g.db = get_db()
    query = g.db.execute(
        "SELECT * FROM transactions WHERE sender=? OR receiver=?",
        (ACCOUNT_NO, ACCOUNT_NO))
    results = []
    for row in query.fetchall():
        isSender = row[0] == ACCOUNT_NO
        results.append(
            dict(
                account=(row[1] if isSender else row[0]),
                amount=(-row[2]) if isSender else row[2],
                comments=row[3],
            ))
    g.db.close()
    return render_template('index.html', transactions=results)


@app.route('/transfer', methods=['POST', 'GET'])
def transfer():
    if request.method == 'POST':
        to_account, amount, comments = (request.form['account'],
                                        request.form['amount'],
                                        request.form['comments'])
        g.db = get_db()
        g.db.execute(
            "INSERT INTO transactions (sender, receiver, amount, comments) VALUES (?, ?, ?, ?)",
            [ACCOUNT_NO, to_account, amount, comments])
        g.db.commit()
        g.db.close()
        return render_template('transfer.html', msg="Transfer successful")

    return render_template('transfer.html')


def get_db():
    return sqlite3.connect(app.database)


if __name__ == "__main__":
    if not os.path.exists(app.database):
        connection = sqlite3.connect(app.database)
        c = connection.cursor()
        c.execute(
            'CREATE TABLE transactions(sender TEXT, receiver TEXT, amount INT, comments TEXT)'
        )
        c.execute(
            'INSERT INTO transactions VALUES("123456", "900900", 100, "Rent")')
        c.execute(
            'INSERT INTO transactions VALUES("798321", "123456", 10000, "Salary")'
        )
        c.execute(
            'INSERT INTO transactions VALUES("789212", "900900", 1000, "Salary")'
        )
        c.execute(
            'INSERT INTO transactions VALUES("900900", "893131", 20, "Interac")'
        )
        connection.commit()
        connection.close()

    app.run(host='0.0.0.0', port=PORT)