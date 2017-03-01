import os
import logging

logging.basicConfig(level=logging.DEBUG)

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}

WTF_CSRF_ENABLED = True

THREADS_PER_PAGE = 2

SECRET_KEY             = '9JWaSYx7VJR£WGQE0Edvcv4rSJbXSRzml8yqhW%b1165ghMJxvWU0WVYNMFBDi'
SECURITY_PASSWORD_SALT = '9SRpHWTIW^rGbyMnIpJZWmmel0X8rVevSljpjw6R720kt*4CwmXXQrmrL1KfGR'

#Scheduler.StartSoup()