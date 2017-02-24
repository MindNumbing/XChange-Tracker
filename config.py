import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY             = '9JWaSYx7VJR£WGQE0Edvcv4rSJbXSRzml8yqhW%b1165ghMJxvWU0WVYNMFBDi'
SECURITY_PASSWORD_SALT = '9SRpHWTIW^rGbyMnIpJZWmmel0X8rVevSljpjw6R720kt*4CwmXXQrmrL1KfGR'

MAIL_SERVER         = 'smtp-mail.outlook.com'
MAIL_PORT           = 587
MAIL_USE_TLS        = True
MAIL_USE_SSL        = False
MAIL_USERNAME       = 'pdfsender@hotmail.com'
MAIL_PASSWORD       = 'Ilovepdf1'
MAIL_DEFAULT_SENDER = 'pdfsender@hotmail.com'