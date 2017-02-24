import timeit
from multiprocessing import cpu_count
from multiprocessing.dummy import Pool as ThreadPool
from flask import render_template, redirect, request, session
import re
from DB import Controls, Validation, Token, Email
from Scheduler import Scheduler
from Scraper import scrape
from app import app
from urllib.request import urlopen

User = None

@app.route('/')
def start():
    session['message'] = None
    return redirect(request.url_root + 'index', code=302)

@app.route('/index')
def index():
    global User

    message = ''
    if session['message'] is not None:
        message = session['message']
        session['message'] = ''

    if User is not 0 and User is not None:
        Data = Controls.GetMessages(User)

        if Data is not None:
            return render_template('index.html', User=User, Message=message, Data=True, AllData=Data[0], LinkedFiles=Data[1], ChangedFiles=Data[2], UnChangedFiles=Data[3])
        else:
            return render_template('index.html', User=User, Message=message)
    else:
        return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global User
    if request.method == "POST":

        username        = request.form['signupUsername']
        email           = request.form['signupEmail']
        password        = request.form['signupPassword']
        confirmpassword = request.form['signupPasswordConfirm']

        result = Validation.ValidateSignUp(username, email, password, confirmpassword)

        if result != None:
            session['message'] = result
        else:
            User = Controls.AddUser(username, email, password)
            #TODO Email user with confirmation email
    return redirect(request.url_root + 'index', code=302)

@app.route('/login', methods=['GET', 'POST'])
def login():
    global User
    if request.method == "POST":

        username = request.form['loginUsername']
        password = request.form['loginPassword']

        result = Validation.ValidateLogIn(username, password)

        if result != None:
            session['message'] = result
        else:
            User = Controls.ValidateUser(username, password)
            if User == 0:
                session['message'] = 'Username or password incorrect'

    return redirect(request.url_root + 'index', code=302)

@app.route('/logout', methods=['POST'])
def logout():
    global User
    if request.method == 'POST':
        User = None
    return redirect(request.url_root + 'index', code=302)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/send', methods=['GET', 'POST'])
def search():
    global User

    if request.method == "POST":
        webpage = request.form['webpage']
        #fileType = request.form['filetype']
        #TODO This needs to be changed so that the user can choose file from a drop down
        fileType = '.pdf'

        #TODO Validate URL

        Files = scrape.MakeSoup(webpage, fileType)
        Files = scrape.CheckForDuplicates(Files)

        numberOfProcesses = (cpu_count() * 2)
        pool = ThreadPool(numberOfProcesses)

        args = []
        for address in Files:
            args.append((address, User))
        Data = pool.map_async(Controls.CheckFileExists, args)

        pool.close()
        pool.join()

        Data = Data.get()

    return redirect(request.url_root + 'index', code=302)

#if __name__ != '__main__':
    #Scheduler.Start()