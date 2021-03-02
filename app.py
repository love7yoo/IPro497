from flask import Flask, render_template
from config import configure_app
from models import *

app = Flask(__name__)
configure_app(app)
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=7000)