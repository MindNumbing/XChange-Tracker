from flask_sqlalchemy import SQLAlchemy
from app.database.db import Base

db = SQLAlchemy()


class User(Base):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(100))
    permission = db.Column(db.Boolean)

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return False

    def is_anonymous(self):
        return False
