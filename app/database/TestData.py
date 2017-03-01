from app.database.db import db_session
from app.auth.model import User
from app.database.model import File

from werkzeug.security import check_password_hash, generate_password_hash

if db_session.query(User).filter_by(username='Steven.Marshall').first():
    user = db_session.query(User).filter_by(username='Steven.Marshall').one()

    db_session.delete(user)
    db_session.commit()

user = User(username='Steven.Marshall', password=generate_password_hash('Password'))
user.authenticated = True

db_session.add(user)
db_session.commit()