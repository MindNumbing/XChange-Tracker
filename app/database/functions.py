from app.database.db import db_session
from hashlib import md5
from urllib.request import urlopen

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