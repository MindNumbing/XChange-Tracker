from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from os import path
from werkzeug.security import generate_password_hash

basedir = path.abspath(path.dirname(__file__))

engine = create_engine('sqlite:///' + path.join(basedir, 'app.db'))
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

metadata = MetaData()

# Define a base model for other database tables to inherit
#class Base(db.Model):

#    __abstract__  = True

#    id            = db.Column(db.Integer, primary_key=True)
#    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
#    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()

    from app.auth.model import User
    from app.database.model import File

    Base.metadata.create_all(bind=engine)