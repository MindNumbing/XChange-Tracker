from flask import render_template, flash, redirect, request, url_for
from app import app
from Scraper import scrape
from DB import Controls
from multiprocessing import cpu_count
from multiprocessing.dummy import Pool as ThreadPool
import timeit
from Scheduler import Scheduler

User = None
Data = None

@app.route('/')
@app.route('/index')
def index():
    global User
    global Data

    if User != 0 or User != None and Data != None:
        return render_template('index.html', User=User, Data=Data)
    elif User != 0 or User != None and Data == None:
        return render_template('index.html', User=User)
    else:
        return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global User
    if request.method == "POST":

        username        = request.form['signupUsername']
        password        = request.form['signupPassword']
        confirmpassword = request.form['signupPasswordConfirm']

        # Username is empty
        if username == None:
            return redirect(request.url_root + 'index', code=302)
        # Password is empty
        elif password == None:
            return redirect(request.url_root + 'index', code=302)
        #Confirm password is empty
        elif confirmpassword == None:
            return redirect(request.url_root + 'index', code=302)
        # If Password and Confirm aren't the same
        elif password != confirmpassword:
            return redirect(request.url_root + 'index', code=302)
        else:
            username = request.form['signupUsername']
            email    = request.form['signupEmail']
            password = request.form['signupPassword']

            User = Controls.AddUser(username, email, password)

            return redirect(request.url_root + 'index', code=302)
    return redirect(request.url_root + 'index', code=302)

@app.route('/login', methods=['GET', 'POST'])
def login():
    global User
    if request.method == "POST":
        # Username is empty
        if request.form['loginUsername'] == None:
            return redirect(request.url_root + 'index', code=302)
        # Password is empty
        elif request.form['loginPassword'] == None:
            return redirect(request.url_root + 'index', code=302)
        else:
            username = request.form['loginUsername']
            password = request.form['loginPassword']

            User = Controls.ValidateUser(username, password)

            return redirect(request.url_root + 'index', code=302)
    return redirect(request.url_root + 'index', code=302)

@app.route('/send', methods=['GET', 'POST'])
def search():
    tic = timeit.default_timer()
    global User
    global Data

    if request.method == "POST":
        webpage = request.form['webpage']

        Files = scrape.MakeSoup(webpage)
        #print('Number of Files : "%s"' % (len(Files)))

        numberOfProcesses = (cpu_count() * 2)
        #print('Number of Processes : "%s"' % (numberOfProcesses))
        pool = ThreadPool(numberOfProcesses)

        #print('Printing files : %s' % (Files))

        args = []
        for file in Files:
            args.append((file, User))
        #print('Args : "%s"' % (args))
        Data = pool.map_async(Controls.CheckFileExists, args)

        pool.close()
        pool.join()

        Data = Data.get()

        #print('Data : "%s"' % (Data))

        toc = timeit.default_timer()
        print(toc - tic)
        return redirect(request.url_root + 'index', code=302)
    return redirect(request.url_root + 'index', code=302)

if __name__ != '__main__':
    Scheduler.StartSoup()