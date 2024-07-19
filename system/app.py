from flask import Flask, render_template
from test_database import get_data_from_database

app = Flask(__name__)

@app.route('/')
def index():
    data = get_data_from_database()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)