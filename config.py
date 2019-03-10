import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgres://ben:123@localhost:5432/test'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'bbland_secret_key'