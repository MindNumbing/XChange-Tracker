from app.database.db import db_session
from app.auth.model import User
from app.database.functions import generate_hash


def setup():
    if db_session.query(User).filter_by(username='Admin').first():
        user = db_session.query(User).filter_by(username='Admin').first()
        db_session.delete(user)
        db_session.commit()

    if db_session.query(User).filter_by(username='User').first():
        user = db_session.query(User).filter_by(username='User').first()
        db_session.delete(user)
        db_session.commit()

    user1 = User(username='Admin', password=generate_hash('Neueda2017'), permission=True)
    user2 = User(username='User', password=generate_hash('Neueda2017'), permission=False)
    db_session.add_all({user1, user2})
    db_session.commit()
