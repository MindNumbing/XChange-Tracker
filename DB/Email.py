from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from os import path
from flask_mail import Mail, Message
from flask import current_app
from app import app
from itsdangerous import URLSafeTimedSerializer

Base = declarative_base()

basedir = path.abspath(path.dirname(__file__))
engine = create_engine('sqlite:///' + path.join(basedir, 'application.db'))

metadata = MetaData(bind=engine)

#Reflect each database table we need to use, using metadata
class Account(Base):
    __table__ = Table('Account', metadata, autoload=True)

class AccountFile(Base):
    __table__ = Table('AccountFile', metadata, autoload=True)

class File(Base):
    __table__ = Table('File', metadata, autoload=True)

# For debugging set to true
engine.echo = False

Session = scoped_session(sessionmaker())
Session.configure(bind=engine)

def GenerateEmails():
    session = Session()

    users = session.query(Account).filter_by(active=True).all()

    Emails = []
    message = ''

    for user in users:
        if user.messages is not None:
            message = ('Hello %s, Here is a list of the files that have changed: \n' % (user.username))
            for line in user.messages:
                if line.startswith('File Changed :'):
                    message = message + line
                    message = message + '\n'
        if message is not None:
            user = (user.email, user.messages)
            Emails.append(user)
            for user in users:
                messages = user.messages
                for line in messages:
                    if line.startswith('File Changed :'):
                        messages.remove(line)

                user.messages = messages
                session.commit(user)
    return Emails

def SendEmails(Emails):
    with app.app_context():
        mail = Mail(current_app)
        with mail.connect() as conn:
            for email in Emails:
                recipient = email[0]
                subject = 'File Checker'
                message = email[1]

                msg = Message(recipients=[recipient],
                              subject=subject,
                              body=message)

                conn.send(msg)

def SendUserToken(userid):
    session = Session()

    user = session.query(Account).filter_by(id=userid).first()

    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    serializer.dumps(user.email, salt=app.config['SECURITY_PASSWORD_SALT'])

    Emails = []

    if user.active == False:
        Recipient = user.email
        #TODO confirm_url = url_for('')
        Message = "Hello, thanks for signing up to our file checker. To confirm your account so that you can be sent emails, please click the link below. \n\n "

        Emails.append((Recipient, Message))
        SendEmails(Emails)
    else:
        return None

    session.close()

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)
    except:
        return False
    return email

def ActivateUser(userid):
    session = Session()

    user = session.query(Account).filter_by(id=userid).first()

    user.active = True

    session.close()