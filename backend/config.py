import os

class Config:
    # ==== Base Directory ====
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # ==== Secret Key ====
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')

    # ==== Uploads ====
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    ALLOWED_PHOTOS = {'jpeg', 'jpg', 'png'}
    ALLOWED_DOCS = {'jpeg', 'jpg', 'png', 'pdf'}

    # ==== Database ====
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:SSNSSN@localhost/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ==== Ensure Upload Directory Exists ====
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
