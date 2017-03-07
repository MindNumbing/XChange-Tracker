from apscheduler.schedulers.background import BackgroundScheduler
from app.scheduler.scheduler import check_files

sched = BackgroundScheduler()
sched.add_job(check_files, 'interval', minutes=5)
sched.start()
