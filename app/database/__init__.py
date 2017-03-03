from app.database.db import metadata, Base, engine
from app.auth.model import User
from app.database.model import File
from app.database import testdata
from sqlalchemy_utils import database_exists
from config import SQLALCHEMY_DATABASE_URI

if not database_exists(SQLALCHEMY_DATABASE_URI):
    file_table = File
    user_table = User
    Base.metadata.create_all(bind=engine)
    testdata.setup()
