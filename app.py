from flask import Flask, render_template, url_for
from config import configure_app
from models import *

app = Flask(__name__)
configure_app(app)
db.init_app(app)

import auth

app.register_blueprint(auth.bp)

@app.route('/')
def index():
    return render_template('index.html')

#@app.route('/')
#def location():
#    return render_template('location/location.html')
#@app.route('/')
#def rnp(): #rules and policies
#    return render_template('rnp/rnp.html')

@app.route('/reservation')
def reservation():
    return render_template('reservation/reservation.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=7000)