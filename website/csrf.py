from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def lottery():
    return render_template('lottery.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8082)
    print('Server started on port 8082')