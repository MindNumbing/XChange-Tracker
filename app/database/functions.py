from app.database.db import db_session
from hashlib import md5
from urllib.request import urlopen
from app.database.model import File

def GetHash(url):
    # print('Getting hash for File : "%s"' % (url))
    BLOCKSIZE = 65536
    hash = md5()

    with urlopen(url) as remote:
        buf = remote.read(BLOCKSIZE)
        while len(buf) > 0:
            hash.update(buf)
            buf = remote.read(BLOCKSIZE)

    return hash.hexdigest()

def GetData():
    Files = db_session.query(File).all()

    data = []

    for file in Files:
        data.append((file.id, file.website, file.file_address, file.date, file.hash))

    return data