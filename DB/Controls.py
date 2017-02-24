from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from os import path
from passlib.hash import pbkdf2_sha512
import hashlib
from urllib.request import urlopen
import random
import copy

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
    session = Session()

    user = session.query(Account).filter_by(username=username).first()

    if user == None:

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
    url    = args[0]
    userid = args[1]

    session = Session()

    if session.query(File).filter_by(address=url).count() > 0:
        # File exists on the database
        user = session.query(Account).filter_by(id=userid).first()
        file = session.query(File).filter_by(address=url).first()

        if session.query(AccountFile).filter_by(account_id=user.id, file_id=file.id).count() > 0:
            #File exists for user
            CompareFile(url, userid)
        else:
            # File does not exist for user
            CreateAssociation(url, userid)
    else:
        #File does not exist
        AddFileToDatabase(url)
        CreateAssociation(url, userid)

    session.close()

def AddFileToDatabase(url):
    #print('Creating File : "%s"' % (url))

    session = Session()

    hash = GetHash(url)

    file = File(address=url, hash=hash)

    session.add(file)
    session.commit()
    session.close()

def CreateAssociation(url, userid):
    #print('Creating association between user "%s" and file "%s"' % (userid, url))
    session = Session()

    user = session.query(Account).filter_by(id=userid).one()
    file = session.query(File).filter_by(address=url).one()
    hash = GetHash(url)

    accountfile = AccountFile(account_id=user.id, file_id=file.id, last_hash=hash)

    session.add(accountfile)
    session.commit()
    session.close()
    AddMessage(userid, 'File Linked,' + str(url))

def CompareFile(url, userid):
    #print('Comparing file for user "%s" and file "%s"' % (userid, url))
    session = Session()

    user = session.query(Account).filter_by(id=userid).first()
    file = session.query(File).filter_by(address=url).first()
    accountfile = session.query(AccountFile).filter_by(account_id=user.id, file_id=file.id).first()
    session.close()

    new_hash = GetHash(url)
    last_hash = accountfile.last_hash

    if new_hash != last_hash:
        session = Session()

        session.query(AccountFile).filter_by(account_id=user.id, file_id=file.id).update(dict(last_hash=new_hash))

        session.commit()
        session.close()

        AddMessage(userid, 'File Changed,' + str(url))
    elif new_hash == last_hash:
        AddMessage(userid, 'File Unchanged,' + str(url))
    session.close()

def SchedulerCompareFile(args):
    userid = args[0]
    fileid = args[1]

    session = Session()

    user = session.query(Account).filter_by(id=userid).first()
    file = session.query(File).filter_by(id=fileid).first()
    accountfile = session.query(AccountFile).filter_by(account_id=user.id, file_id=file.id).first()
    session.close()

    url = file.address

    new_hash = GetHash(file.address)
    last_hash = accountfile.last_hash

    #print('Last Hash "%s" \nNew Hash "%s"' % (last_hash,new_hash))

    if new_hash != last_hash:
        session = Session()

        session.query(AccountFile).filter_by(account_id=user.id, file_id=file.id).update(dict(last_hash=new_hash))

        session.commit()
        session.close()

        AddMessage(userid, 'File Changed,' + str(url))
    elif new_hash == last_hash:
        AddMessage(userid, 'File Unchanged,' + str(url))

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

def GetAllUsers():
    print('Displaying all User Records')
    session = Session()

    userlist = session.query(Account).all()
    users = []

    #for user in userlist:
    #    print('User Message : "%s"' % (user.messages))
    #    users.append(user.username)

    for user in userlist:
        print(user)

    for user in userlist:
        print(user.messages)

def GetAllFiles():
    print('Displaying all File Records')
    session = Session()

    filelist = session.query(File).all()
    files = []

    #for file in filelist:
    #    print('File : "%s"' % (file))
    #    files.append(file.url)

    for file in filelist:
        print(file.address)

def GetAllAssocations():
    session = Session()

    accountfiles = session.query(AccountFile)

    associations = []
    for accountfile in accountfiles:
        associations.append((accountfile.account_id, accountfile.file_id))

    session.close()

    return associations

def AddMessage(userid, Message):
    session = Session()

    user = session.query(Account).filter_by(id=userid).first()

    if type(user.messages) is type(None):
        print('Some message')
        session.query(Account).filter_by(id=userid).update(dict(messages=Message))
        session.commit()
        session.close()
    else:
        print('None message')
        FinalMessage = user.messages + ',' + Message
        session.query(Account).filter_by(id=userid).update(dict(messages=FinalMessage))
        session.commit()
        session.close()


def GetMessages(userid):
    session = Session()

    if userid is not 0 or None:
        user = session.query(Account).filter_by(id=userid).first()
        if user is not None:
            if user.messages is not '' and user.messages is not None:
                messages = user.messages.split(',')

                session.query(Account).filter_by(id=userid).update(dict(messages=None))
                session.commit()
                session.close()

                messages = iter(messages)

                Data = []

                AllData        = []
                LinkedFiles    = []
                ChangedFiles   = []
                UnChangedFiles = []

                Data = zip(messages, messages)

                Data1 = list(Data)
                Data2 = list(Data)
                Data3 = list(Data)
                Data4 = list(Data)

                for item in Data1:
                    #print('Data 1 : "%s" "%s"' % (str(item[0]), str(item[1])))
                    AllData.append(item)

                for item in Data2:
                    #print('Data 2 : "%s" "%s"' % (str(item[0]), str(item[1])))
                    if item[0] == 'File Linked':
                        LinkedFiles.append(item)

                for item in Data3:
                    #print('Data 3 : "%s" "%s"' % (str(item[0]), str(item[1])))
                    if item[0] == 'File Changed':
                        ChangedFiles.append(item)

                for item in Data4:
                    print('Data 4 : "%s" "%s"' % (str(item[0]), str(item[1])))
                    if item[0] == 'File Unchanged':
                        print('Got unchanged')
                        UnChangedFiles.append(item)

                Data = []

                Data.append(AllData)
                print(AllData)
                Data.append(LinkedFiles)
                print(LinkedFiles)
                Data.append(ChangedFiles)
                print(ChangedFiles)
                Data.append(UnChangedFiles)
                print(UnChangedFiles)

                return Data

    session.close()

def CheckUser(userid):
    session = Session()

    user = session.query(Account).filter_by(id=userid).first()

    session.close()

    return user.active

def ConfirmUser(userid):
    session = Session()

    user = session.query(Account).filter_by(id=userid).first()

    user.active = True

    session.commit(user)

    session.close()

if __name__ == '__main__':
    GetAllFiles()
    GetAllUsers()