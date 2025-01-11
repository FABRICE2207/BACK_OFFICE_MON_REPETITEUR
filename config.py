import os
import psycopg2
import pymssql


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'send-me-a-message'
    PWD_TRANS_SECRET_KEY = '98YniuD38tHOrLGnnL7c71uePflvD1XZF2L9GrDzEks='
    DB_URL = os.environ.get('DB_URL')
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_NAME = os.environ.get('DB_NAME')
    UPLOADS_DIR = 'src/static/'
    TEST_HTTP_API_URLS = os.environ.get('TEST_HTTP_API_URLS')
    TEST_HTTPS_API_URLS = os.environ.get('TEST_HTTPS_API_URLS')
    SMS_API_USER = os.environ.get('SMS_API_USER')
    SMS_API_PASSWORD = os.environ.get('SMS_API_PASSWORD')
    OMP_FRONT_LINK = ''
    PO_MAIL_SUBJECT_PREFIX = ''
    PO_MAIL_SENDER = ''
    DATABASE_URL = 'postgresql+psycopg2://postgres:admin@127.0.0.1/db_mon_repetiteur'.format(user
        =DB_USER, pw=DB_PASSWORD, url=DB_URL, db=DB_NAME)
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_JWT_SECRET_KEY = 'd7af55bdd28eae455e161ee3'

config = {
    "development": Config
}