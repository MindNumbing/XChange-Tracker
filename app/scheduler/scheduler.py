from app.database.db import db_session
from datetime import datetime
from app.database.functions import get_hash
from app.database.model import File


def check_files():
    files = db_session.query(File).all()

    for file in files:
        compare_files(file.id)


def compare_files(fileid):
    file = db_session.query(File).filter_by(id=fileid).first()

    new_hash = get_hash(file.file_address)

    if file.hash is not None:
        if new_hash != file.hash:
            file.hash = new_hash
            file.date = datetime.now()
            db_session.commit()
    else:
        file.hash = new_hash
        db_session.commit()
