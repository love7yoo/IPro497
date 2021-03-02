# coding:utf-8
from flask_sqlalchemy import SQLAlchemy
import os
import base64

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))

    def __init__(self, username, password):
        self.username = username
        self.password = password
