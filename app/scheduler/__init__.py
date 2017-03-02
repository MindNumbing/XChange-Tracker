from apscheduler.schedulers.background import BackgroundScheduler
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import cpu_count
from app.database.db import db_session

from datetime import datetime
from app.database.functions import GetHash
from app.database.model import File

from app.scheduler.Scheduler import CheckFiles

sched = BackgroundScheduler()
sched.add_job(CheckFiles, 'interval', seconds=20)
sched.start()