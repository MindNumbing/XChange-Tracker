# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app.database.db import Base

db = SQLAlchemy()

# Define a User model
class User(Base):
    __tablename__ = 'User'
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(64), index=True, unique=True)
    password      = db.Column(db.String(40), index=True, unique=True)

    #files = db.relationship('File', backref='creator', lazy='dynamic')

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True
        #return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def __repr__(self):
        return '<User %r>' % (self.username)

    def __init__(self, username, password):
        self.username      = username
        self.password      = password