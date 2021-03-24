from flask import Flask, render_template, url_for, request, session
from config import configure_app
from models import *
import json
from datetime import datetime

app = Flask(__name__)
configure_app(app)
db.init_app(app)

import auth

app.register_blueprint(auth.bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/location')
def location():
    return render_template('location/location.html')

@app.route('/rules_and_policies')
def rules_and_policies(): #rules and policies
    return render_template('rules_and_policies/rules_and_policies.html')

@app.route('/reservation')
def reservation():
    return render_template('reservation/reservation.html')

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
    res = db.session.query(Reservation).join(Location).filter(Location.building == building).filter(Location.room == room).all()

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

@app.route('/reserve', methods = ['POST', 'GET'])
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
        return render_template('reservation/success.html')
    else:
        return render_template('reservation/fail.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=7000)