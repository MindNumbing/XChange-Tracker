from apscheduler.schedulers.background import BackgroundScheduler
from DB import Controls
from multiprocessing.dummy import Pool as ThreadPool

def StartSoup():
    sched = BackgroundScheduler()
    sched.add_job(CheckFiles, 'interval', minutes=60)
    sched.start()

def CheckFiles():
    pool = ThreadPool(4)

    files = Controls.GetAllFiles()

    users = pool.map_async(Controls.GetAllAssocations, (files))

    print('Multi Result : %s' + users)

    pool.close()
    pool.join()

    #files = Controls.GetAllFiles()
    #for file in files:
    #    users = Controls.GetAllAssocations(file)
    #    for user in users:
    #        Controls.CompareFile(file, users)