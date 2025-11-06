import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgresql@localhost/studentdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')
