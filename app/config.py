import os
from datetime import timedelta
from re import DEBUG

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'very_secret_key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://doadmin:AVNS_-iK8H6-2D_M_AJ7aSWn@db-postgresql-sfo3-petru-webapp-do-user-3433219-0.c.db.ondigitalocean.com:25060/petru-database?sslmode=require'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=12)
    UPLOAD_PATH_IMAGE = os.path.join(basedir, 'static', 'images')
    UPLOAD_PATH_PDF = os.path.join(basedir, 'static', 'pdf')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}