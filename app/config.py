import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Secret key for signing cookies
    SECRET_KEY = os.getenv('SECRET_KEY')

    # Database URI
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session settings
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=12)

    # File upload paths
    UPLOAD_PATH_IMAGE = os.path.join(basedir, 'static', 'images')
    UPLOAD_PATH_PDF = os.path.join(basedir, 'static', 'pdf')

    # Digital Ocean Spaces 
    DO_SPACES_REGION = os.getenv('DO_SPACES_REGION')
    DO_SPACES_BUCKET = os.getenv('DO_SPACES_BUCKET')
    DO_SPACES_ENDPOINT_URL = os.getenv('DO_SPACES_ENDPOINT_URL')
    DO_SPACES_CDN_BASE_URL = os.getenv('DO_SPACES_CDN_BASE_URL')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

    # Allowed extensions for uploads
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}