from flask_sqlalchemy import SQLAlchemy
from app.database.db import Base

db = SQLAlchemy()


class File(Base):
    __tablename__ = 'File'
    id = db.Column(db.Integer, primary_key=True)
    website = db.Column(db.String(64))
    file_address = db.Column(db.String(1024), unique=True)
    date = db.Column(db.DateTime)
    hash = db.Column(db.String(32))
