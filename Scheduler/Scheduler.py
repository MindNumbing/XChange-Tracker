from apscheduler.schedulers.background import BackgroundScheduler
from DB import Controls, Email
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import cpu_count

def Start():
    sched = BackgroundScheduler()
    sched.add_job(CheckFiles, 'interval', minutes=0.2)
    sched.add_job(NotifyByEmail, 'interval', minutes=0.2)
    sched.start()

def CheckFiles():
    associations = Controls.GetAllAssocations()

    numberOfProcesses = (cpu_count() * 2)
    pool = ThreadPool(numberOfProcesses)

    args = []
    for association in associations:
        args.append((association[0], association[1]))

    Data = pool.map_async(Controls.SchedulerCompareFile, args)

    pool.close()
    pool.join()

def NotifyByEmail():
    Emails = Email.GenerateEmails()
    Email.SendEmails(Emails)