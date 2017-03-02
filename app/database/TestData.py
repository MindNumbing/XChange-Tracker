from app.database.db import db_session
from app.auth.model import User
from app.database.model import File

from werkzeug.security import check_password_hash, generate_password_hash

if db_session.query(User).filter_by(username='Admin').first():
    user = db_session.query(User).filter_by(username='Admin').first()
    db_session.delete(user)
    db_session.commit()

if db_session.query(User).filter_by(username='User').first():
    user = db_session.query(User).filter_by(username='User').first()
    db_session.delete(user)
    db_session.commit()

user1 = User(username='Admin', password=generate_password_hash('Neueda2017'), permission='Admin')
user2 = User(username='User', password=generate_password_hash('Neueda2017'), permission='User')
db_session.add_all({user1, user2})
db_session.commit()