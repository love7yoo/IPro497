import webbrowser

from selenium import webdriver

from flask import Flask, render_template, url_for, request, session, g
from werkzeug.utils import redirect

from config import configure_app
from models import *
import json
from datetime import datetime
from flask_mail import Mail, Message

from google.oauth2 import id_token
from google.auth.transport import requests

app = Flask(__name__)
configure_app(app)
db.init_app(app)
mail = Mail(app)

import auth

app.register_blueprint(auth.bp)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tokensignin', methods=['GET', 'POST'])
def tokensignin():
    if request.method == 'POST':
        # (Receive token by HTTPS POST)
        token = request.form["idtoken"]

        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(),
                                                  '986356076768-il18j7f2ep676n49564027qqv6h6l7a7.apps.googleusercontent.com')
            # If auth request is from a G Suite domain:
            if idinfo['hd'] != ('hawk.iit.edu' or 'iit.edu'):
                return render_template('index.html')

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            userid = idinfo['sub']
            email_address = idinfo['email']
            name = idinfo['name']

            # check the user previously logged in
            user = User.query.filter_by(email_address=email_address).first()

            # if the user logged in first time, add to db
            if user is None:
                new_user = User(email_address, userid, 'password', name)
                db.session.add(new_user)
                db.session.commit()
                user = User.query.filter_by(email_address=email_address).first()

            # logging in
            session.clear()
            session['user_email_address'] = user.email_address
            webbrowser.open("http://localhost:7000")
            

        except ValueError:
            # Invalid token
            pass

    return render_template('index.html')


@app.before_request
def load_logged_in_user():
    email_address = session.get('user_email_address')
    if email_address is None:
        g.user = None
    else:
        g.user = User.query.filter_by(email_address=email_address).first()


@app.route('/loading')
def loading():
    return render_template('loading/loading.html')

@app.route('/location')
def location():
    return render_template('location/location.html')


@app.route('/rules_and_policies')
def rules_and_policies():  # rules and policies
    return render_template('rules_and_policies/rules_and_policies.html')


@app.route('/reservation')
def reservation():
    return render_template('reservation/reservation.html')


@app.route('/room_report')
def report():
    return render_template('rules_and_policies/report.html')


@app.route('/room_report_success')
def r_s():
    return render_template('rules_and_policies/r_s.html')


@app.route('/location_list')
def location_list():
    location_list = db.session.query(Location).all()
    data = []
    for row in location_list:
        tmp = dict()
        tmp['building'] = row.building
        tmp['room'] = row.room
        data.append(tmp)
    return json.dumps(data)


@app.route('/cur_reservation')
def cur_location():
    loc = request.args.get("location")
    building = loc.split('|')[0]
    room = loc.split('|')[1][:-1]
    res = db.session.query(Reservation).join(Location).filter(Location.building == building).filter(
        Location.room == room).all()

    data = []
    for temp in res:
        out = dict()
        out['email_address'] = temp.email_address
        out['building'] = building
        out['room'] = room
        out['start'] = str(temp.reservation_start)
        out['end'] = str(temp.reservation_end)
        out['reservation'] = temp.reservation_status
        data.append(out)
    # print(data)
    return json.dumps(data)


@app.route('/reserve', methods=['POST', 'GET'])
def reserve():
    if request.method == 'POST':
        res = (request.form).to_dict(flat=False)

        building = res['Location'][0].split('|')[0]
        room = res['Location'][0].split('|')[1][:-1]

        info = db.session.query(Location).filter(Location.building == building).filter(Location.room == room).first()

        time_start = datetime.strptime(res['reservation_start'][0], '%Y-%m-%dT%H:%M')
        time_end = datetime.strptime(res['reservation_end'][0], '%Y-%m-%dT%H:%M')

        user_email_address = session.get('user_email_address')

        query = Reservation(
            email_address=user_email_address,
            location_id=info.id,
            reservation_start=time_start,
            reservation_end=time_end,
            reservation_status=1
        )

        db.session.add(query)
        db.session.commit()

        # send_email()

        return render_template('reservation/success.html')
    else:
        return render_template('reservation/fail.html')


@app.route('/send_email')
def send_email():
    msg = Message('Your HawkSpot Reservation is Confirmed!', recipients=[session.get('user_email_address')])
    msg.body = "TEST EMAIL"
    mail.send(msg)
    return "Message sent!"


if __name__ == '__main__':
    app.run(host='localhost', port=7000)
