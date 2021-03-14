# coding:utf-8
from flask_sqlalchemy import SQLAlchemy
import os
import base64

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    email_address = db.Column(db.String(50), primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(20), nullable=False)

    def __init__(self, email_address, username, password, name):
        self.email_address = email_address
        self.username = username
        self.password = password
        self.name = name

class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    building = db.Column(db.String(30), nullable=False)
    room = db.Column(db.String(10), nullable=False)
    reservation_status = db.Column(db.Boolean())
    reservation_length = db.Column(db.Integer())

class Reservation(db.Model):
    __tablename__ = 'reservation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email_address = db.Column(db.String(50), db.ForeignKey('user.email_address'))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    reservation_start = db.Column(db.DATETIME())
    reservation_end = db.Column(db.DATETIME())

class Open_hours(db.Model):
    __tablename__ = 'open_hours'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Day = db.Column(db.INTEGER())
    start_time = db.Column(db.DATETIME())
    end_time = db.Column(db.DATETIME())