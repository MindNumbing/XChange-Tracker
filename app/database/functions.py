from app.database.db import db_session
from app.database.model import File
from app.auth.model import User
from hashlib import md5
from urllib.request import urlopen
from datetime import datetime
from passlib.hash import pbkdf2_sha512
import random
from sqlalchemy import desc
import re

def get_hash(url):
    block_size = 65536
    md5_hash = md5()
    try:
        with urlopen(url) as remote:
            buf = remote.read(block_size)
            while len(buf) > 0:
                md5_hash.update(buf)
                buf = remote.read(block_size)
        return md5_hash.hexdigest()
    except ValueError:
        return None


def get_data():
    data = []

    files = db_session.query(File).order_by(File.date.desc()).all()

    for file in files:
        data.append((file.id, file.website, file.file_name, file.file_address, datetime.strftime(file.date, '%d/%b/%Y - %H:%M'),
                    file.hash))

    return data


def generate_hash(password):
    return pbkdf2_sha512.using(salt_size=64, rounds=64000 + random.randint(0, 24000)).hash(password)


def verify_password(username, password):
    user = db_session.query(User).filter_by(username=username).first()
    if pbkdf2_sha512.verify(password, user.password):
        return True

def get_file_name(file):
    name = re.findall('\/[^//]*$', file)[0]
    name = re.compile('\w', name)
    return name
