from sqlalchemy import create_engine, MetaData, Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship, backref
from os import path

Base = declarative_base()

basedir = path.abspath(path.dirname(__file__))
engine = create_engine('sqlite:///' + path.join(basedir, 'application.db'))

metadata = MetaData(bind=engine)

class Account(Base):
    __tablename__ = 'Account'
    id           = Column(Integer, primary_key=True)
    username     = Column(String(64), unique=True)
    email        = Column(String(254), unique=True)
    password     = Column(String(1024))
    active       = Column(Boolean())
    messages     = Column(String())

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
    file_id       = Column(Integer, ForeignKey('File.id')   , primary_key=True)
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

Base.metadata.create_all(engine)