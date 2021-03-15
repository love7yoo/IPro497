import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from models import *

# from flask_sqlalchemy import SQLAlchemy

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email_address = request.form['email_address']
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif User.query.filter_by(username=username).first() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            new_user = User(email_address, username, generate_password_hash(password), name)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = User.query.filter_by(username=username).first()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_email_address'] = user.email_address
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_email_address = session.get('user_email_address')

    if user_email_address is None:
        g.user = None
    else:
        g.user = User.query.filter_by(email_address=user_email_address).first()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@bp.route('/userinfo')
def userinfo():
    return render_template('auth/userinfo.html')


@bp.route('/change_password', methods=['POST', 'GET'])
def change_password():
    if g.user is None:
        redirect(url_for('auth.userinfo'))
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_new_password = request.form['confirm_new_password']
        error = None

        if not check_password_hash(g.user.password, current_password):
            error = 'Incorrect current password.'
        elif new_password != confirm_new_password:
            error = 'New passwords do not match.'

        if error is None:
            user = User.query.filter_by(email_address=g.user.email_address).first()
            user.password = generate_password_hash(new_password)
            g.user = user
            db.session.commit()
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/change_password.html')
