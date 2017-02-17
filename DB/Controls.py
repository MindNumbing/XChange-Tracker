from sqlalchemy import *
from sqlalchemy.orm import mapper, sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import os
from passlib.hash import pbkdf2_sha512
import hashlib
from urllib.request import urlopen
import random
import threading
from app import views

Base = declarative_base()

basedir = os.path.abspath(os.path.dirname(__file__))
engine = create_engine('sqlite:///' + os.path.join(basedir, 'application.db'))

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

def AddUser(username, email, password):
    #print('Adding User : "%s" with the Email : "%s"' % (username, email))

    session = Session()

    rounds = random.randint(1, 20000)
    hash   = pbkdf2_sha512.using(salt_size=16, rounds=64000 + rounds).hash(password)

    user = Account(username=username, email=email, password=hash)

    session.add(user)
    session.commit()

    user = session.query(Account).filter_by(username=username).first()

    id = user.id

    session.close()

    if user != None:
        return id
    else:
        return 0

def ValidateUser(username, password):
    #print('Validating User : "%s"' % (username))

    session = Session()

    user = session.query(Account).filter_by(username=username).first()

    if user == None:
        print('NoValuesFound')

        session.close()

        return False

    hash = user.password

    isValid = pbkdf2_sha512.verify(password, hash)

    id = user.id

    session.close()

    if isValid:
        return id
    else:
        return 0

def CheckFileExists(args):
    # This function checks if the file already exists on the database.
    # If it does already exist:
    #   it runs a check on whether the user is associated
    #   if the file is associated with the user, it checks whether there have been changes to the file
    #   if the file is not associated with the user, it creates an association with the
    # if it don't already exist, it adds the file to the database and creates an association for the user

    url    = args[0]
    userid = args[1]

    #print('Checking File : "%s" for User : "%s"' % (url, userid))

    # Creates a session on the database
    session = Session()

    if session.query(File).filter_by(address=url).count() > 0:
        # File exists on the database
        user = session.query(Account).filter_by(id=userid)
        file = session.query(File).filter_by(address=url)

        if session.query(AccountFile).filter_by(account_id=user.id, file_id=file.id).count > 0:
            #File exists for user
            result = CompareFile(url, userid)
        else:
            # File does not exist for user
            result = CreateAssociation(url, userid)
    else:
        #File does not exist
        AddFileToDatabase(url)
        result = CreateAssociation(url, userid)

    session.close()
    return result

def AddFileToDatabase(url):
    #print('Creating File : "%s"' % (url))

    session = Session()

    hash = GetHash(url)

    file = File(address=url, hash=hash)

    session.add(file)
    session.commit()
    session.close()

def CreateAssociation(url, userid):
    #print('Creating an association between File : "%s" for User : "%s' % (url, userid))

    session = Session()

    user = session.query(Account).filter_by(id=userid).one()
    file = session.query(File).filter_by(address=url).one()
    hash = GetHash(url)

    accountfile = AccountFile(account_id=user.id, file_id=file.id, last_hash=hash)

    session.add(accountfile)
    session.commit()
    session.close()
    return (url, 'File Linked')

def CompareFile(url, userid):
    #print('Comparing file : "%s" for user : "%s' % (url, userid))

    session = Session()

    user = session.query(Account).filter_by(id=userid).first()
    file = session.query(File).filter_by(address=url).first()

    accountfile = session.query(AccountFile).filter_by(account_id=user.id, file_id=file.id).first()

    new_hash = GetHash(url)
    last_hash = accountfile.last_hash

    if new_hash != last_hash:
        #hash has changed
        #print('File : %s has changed. New Hash : "%s". Old Hash : "%s"' % (url, new_hash, last_hash))
        #Store new hash as last_hash
        accountfile.last_hash = file.hash
        session.commit()
        session.close()
        return (url, 'File has changed')
    elif new_hash != last_hash:
        #Hash has not changed
        #print('File : %s has not changed. New Hash : "%s". Old Hash : "%s"' % (url, new_hash, last_hash))
        return (url, 'File not changed')
    session.close()

def GetHash(url):
    #print('Getting hash for File : "%s"' % (url))
    BLOCKSIZE = 65536
    hash = hashlib.md5()

    with urlopen(url) as remote:
        buf = remote.read(BLOCKSIZE)
        while len(buf) > 0:
            hash.update(buf)
            buf = remote.read(BLOCKSIZE)

    return hash.hexdigest()

def GetAllFiles():
    #print('Displaying all File Records')
    session = Session()

    filelist = session.query(File)
    files = []

    for file in filelist:
        #print('File : "%s"' % (file))
        files.append(file.url)

    return files

def GetAllAssocations(url):
    #print('Getting all associations of File : "%s"' % (url))

    session = Session()

    file = session.query(File).filter_by(address=url)
    accountfiles = session.query(AccountFile).filter_by(file_id=file.id).all()

    users = []

    for accountfile in accountfiles:
        #print('Account File : "%s"' % (accountfile))
        users.append(accountfile.account_id)

    session.close()

    return users