import os

class BaseConfig(object):
    pass

class DevConfig(BaseConfig):
    DEBUG = True
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS=False

config = {
    "default": "config.DevConfig"
}

def configure_app(app):
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    app.config.from_object(config[config_name])
