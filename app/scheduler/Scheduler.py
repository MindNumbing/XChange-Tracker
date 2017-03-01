from apscheduler.schedulers.background import BackgroundScheduler
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import cpu_count
from app.database.db import db_session

from datetime import datetime
from app.database.functions import GetHash
from app.database.model import File

def CheckFiles():
    Files = db_session.query(File).all()

    numberOfProcesses = (cpu_count() * 2)

    pool = ThreadPool(numberOfProcesses)

    pool.map_async(CompareFile, Files)

def CompareFile(fileid):
    file = db_session.query(File).filter_by(id=fileid).first()

    new_hash = GetHash(file.address)
    last_hash = file.hash

    if new_hash != last_hash:
        file.hash = new_hash
        file.current_date = datetime.now()

        db_session.commit()

if __name__ != '__main__':
    sched = BackgroundScheduler()
    sched.add_job(CheckFiles, 'interval', hours=1)
    sched.start()