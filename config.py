# Config.py


from flask import Config

class Config(object):
    SECRET_KEY = 'una_llave_aleatoria'

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'