import os

class Config(object):
    #SQLALCHEMY_DATABASE_URI = 'postgres://ben:123@localhost:5432/test'
    SQLALCHEMY_DATABASE_URI = "postgres://rlsnoflrajakev:1f09eedf5b6fd5617e280533488b012491f804eef86401e80d15897f16c202e2@ec2-184-73-216-48.compute-1.amazonaws.com:5432/d68ejemp44fve"
    #SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'bbland_secret_key'