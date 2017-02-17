import sqlalchemy
import os
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base

basedir = os.path.abspath(os.path.dirname(__file__))
db = sqlalchemy.create_engine('sqlite:///' + os.path.join(basedir, 'application.db'))

Base = declarative_base()

class Account(Base):
    __tablename__ = 'Account'
    id           = Column(Integer, primary_key=True)
    username     = Column(String(64), unique=True)
    email        = Column(String(254), unique=True)
    password     = Column(String(1024))
    active       = Column(Boolean())

    # association proxy of "account_Files" collection
    # to "file" attribute
    files = association_proxy('account_Files', 'file')

    def __init__(self, username, email, password):
        self.username = username
        self.email    = email
        self.password = password
        self.active   = False

class AccountFile(Base):
    __tablename__ = 'AccountFile'
    account_id    = Column(Integer, ForeignKey('Account.id'), primary_key=True)
    file_id       = Column(Integer, ForeignKey('File.id'), primary_key=True)
    last_hash     = Column(String(32))

    # bidirectional attribute/collection of "account"/"account_Files"
    account = relationship(Account,
                backref=backref("account_Files",
                                cascade="all, delete-orphan")
            )

    # reference to the "File" object
    file = relationship("File")

    def __init__(self, account, file, last_hash):
        self.account   = account
        self.file      = file
        self.last_hash = last_hash

class File(Base):
    __tablename__ = 'File'
    id            = Column(Integer, primary_key=True)
    address       = Column('address', String(128))
    hash          = Column('hash', String(32))

    def __init__(self, address, hash):
        self.address = address
        self.hash    = hash

    def __repr__(self):
        return 'File(%s)' % repr(self.address)

Base.metadata.create_all(db)

Session = sessionmaker(bind=db)
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