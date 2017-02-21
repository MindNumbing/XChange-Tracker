from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from os import path
from passlib.hash import pbkdf2_sha512
import hashlib
from urllib.request import urlopen
import random

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

session = Session()

#Create two accounts
account1 = Account('account1', 'Email1', 'Password1')
account2 = Account('account2', 'Email2', 'Password2')

session.add_all([account1, account2])
session.commit()

#Create two files
file1 = File('File1', 'hash1')
file2 = File('File2', 'hash2')

session.add_all([file1, file2])
session.commit()

#Create four associations
#Get the accounts
account1 = session.query(Account).filter_by(id=1).first()
account2 = session.query(Account).filter_by(id=2).first()

#Get the files
file1 = session.query(File).filter_by(id=1).first()
file2 = session.query(File).filter_by(id=2).first()

#Create the associations
assoc1 = AccountFile(account1, file1, 'special1')
assoc2 = AccountFile(account1, file2, 'special2')
assoc3 = AccountFile(account2, file1, 'special3')
assoc4 = AccountFile(account2, file2, 'special4')

session.add_all([assoc1, assoc2, assoc3, assoc4])
session.commit()

#Get the accounts
account1 = session.query(Account).filter_by(id=1).first()
account2 = session.query(Account).filter_by(id=2).first()

#Get the files
file1 = session.query(File).filter_by(id=1).first()
file2 = session.query(File).filter_by(id=2).first()

#Get the associations
assoc1 = session.query(AccountFile).filter_by(account_id=1, file_id=1).first()
assoc2 = session.query(AccountFile).filter_by(account_id=1, file_id=2).first()
assoc3 = session.query(AccountFile).filter_by(account_id=2, file_id=1).first()
assoc4 = session.query(AccountFile).filter_by(account_id=2, file_id=2).first()

print()
print('Accounts :-')
print()
accounts = session.query(Account)
for account in accounts:
    print('- Account : "%s" is called : "%s". Has the email : "%s" and password : "%s". It is linked to the files : "%s"' % (account.id, account.username, account.email, account.password, account.files))

print()
print('Files :-')
print()
files = session.query(File)
for file in files:
    print('- File : "%s" and has the address : "%s" and the hash : "%s"' % (file.id, file.address, file.hash))

print()
print('Account Files :-')
print()
accountFiles = session.query(AccountFile)
for accountFile in accountFiles:
    print('- Account_File has the account : "%s", the file : "%s" and the special key : "%s"' % (accountFile.account_id, accountFile.file_id, accountFile.last_hash))

session.close()