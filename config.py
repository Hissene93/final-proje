import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'votre-cle-secrete-complexe-ici'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/student_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False