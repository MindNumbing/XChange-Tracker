from apscheduler.schedulers.background import BackgroundScheduler
from DB import Controls
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import cpu_count

def StartSoup():
    sched = BackgroundScheduler()
    sched.add_job(CheckFiles, 'interval', seconds=20)
    sched.start()
    print('Scheduler has been started')

def CheckFiles():
    associations = Controls.GetAllAssocations()
    print('Number of Files : "%s"' % (len(associations)))

    numberOfProcesses = (cpu_count() * 2)
    print('Number of Processes : "%s"' % (numberOfProcesses))
    pool = ThreadPool(numberOfProcesses)

    print('Printing files : %s' % (associations))

    args = []
    for association in associations:
        args.append((association[0], association[1]))
    print('Args : "%s"' % (args))
    Data = pool.map_async(Controls.SchedulerCompareFile, args)

    print('Gonna Close')

    pool.close()
    pool.join()

    Data = Data.get()

    for file in Data:
        print('File Address : "%s" File Message : "%s" ' % (file[0], file[1]))