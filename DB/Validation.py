from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from os import path
from flask_mail import Mail, Message
from flask import current_app
from app import app
import re
from DB import Validation

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

def CheckUsernameUnique(username):

    session = Session()

    user = session.query(Account).filter_by(username=username).first()

    session.close()

    if user is None:
        return True
    else:
        return False

def CheckEmailUnique(email):

    session = Session()

    user = session.query(Account).filter_by(email=email).first()

    session.close()

    if user is None:
        return True
    else:
        return False

def ValidateSignUp(username, email, password, confirmpassword):

    if username == None:
        return "Username is empty"
    elif email == None:
        return "Email is empty"
    elif password == None:
        return "Password is empty"
    elif confirmpassword == None:
        return "Confirm Password is empty"


    elif Validation.CheckUsernameUnique(username) == False:
        return "Username already exists"
    elif Validation.CheckEmailUnique(email) == False:
        return "Email already exists"

    elif len(password) < 10:
        return "Password must be at least 10 characters"
    elif not re.search('\d', password):
        return 'Password must contain one number'
    elif not re.search('[A-Z]', password):
        return 'Password must contain a capital letter'
    elif password != confirmpassword:
        return "Password and Confirm password do not match"

    return None

def ValidateLogIn(username, password):

    if username == None:
        return "Username is empty"
    elif password == None:
        return "Password is empty"

    return None

