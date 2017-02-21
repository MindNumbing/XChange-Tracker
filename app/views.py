import timeit
from multiprocessing import cpu_count
from multiprocessing.dummy import Pool as ThreadPool
from flask import render_template, redirect, request, session
import re
from DB import Controls
from Scheduler import Scheduler
from Scraper import scrape
from app import app

User = None
Data = None

@app.route('/')
def start():
    session['error'] = None
    return redirect(request.url_root + 'index', code=302)

@app.route('/index')
def index():
    global User
    global Data

    message = ''
    if session['error'] is not None:
        app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
        message = session['error']
        session['error'] = ''

    if User != 0 or User != None and Data != None:
        return render_template('index.html', User=User, Message=message, Data=Data)
    elif User != 0 or User != None and Data == None:
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

        digitcheck      = contains_digits(password)
        capscheck       = contains_uppercase(password)
        common          = contains_common(password)

        # Username is empty
        if username == None:
            session['error'] = "Username is empty"
            return redirect(request.url_root + 'index', code=302)
        elif email == None:
            session['error'] = "Email is empty"
            return redirect(request.url_root + 'index', code=302)
        elif Controls.CheckUsernameUnique(username) == False:
            session['error'] = "Username already exists"
            return redirect(request.url_root + 'index', code=302)
        elif Controls.CheckEmailUnique(email) == False:
            session['error'] = "Email already exists"
            return redirect(request.url_root + 'index', code=302)
        elif capscheck == False:
            session['error'] = "Password must contain a capital letter"
            return redirect(request.url_root + 'index', code=302)
        elif digitcheck != True:
            session['error'] = "Must have a number"
            return redirect(request.url_root + 'index', code=302)
        elif len(str(password)) < 10:
            session['error'] = "Password must be at least 10 characters"
            return redirect(request.url_root + 'index', code=302)
        elif common != False:
            session['error'] = "Password is too common"
            return redirect(request.url_root + 'index', code=302)
        elif password == None:
            session['error'] = "Password is empty"
            return redirect(request.url_root + 'index', code=302)
        elif confirmpassword == None:
            session['error'] = "Confirm Password is empty"
            return redirect(request.url_root + 'index', code=302)
        elif password != confirmpassword:
            session['error'] = "Password and Confirm password do not match"
            return redirect(request.url_root + 'index', code=302)
        else:
            username = request.form['signupUsername']
            email    = request.form['signupEmail']
            password = request.form['signupPassword']

            User = Controls.AddUser(username, email, password)
            if User !=0:
                Controls.ConfirmEmail(email, username)
                return redirect(request.url_root + 'index', code=302)
            else:
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

@app.route('/logout', methods=['POST'])
def logout():
    global User
    if request.method == 'POST':
        User = None
    return redirect(request.url_root + 'index', code=302)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/404', methods=['GET'])
def page_not_found():
    return render_template('404.html')

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
        for address in Files:
            args.append((address, User))
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

#Validation Start
#functions for password validation
def contains_digits(d):
    _digits = re.compile('\d')
    print(bool(_digits.search(d)))
    return bool(_digits.search(d))

#making sure password contains an uppercase letter
def contains_uppercase(password):
    capitals = True
    letters = password
    uppers = [l for l in letters if l.isupper()]
    if len(uppers) == 0:
        capitals = False
    return bool(capitals)

#list of common passwords that users arent allowed
def contains_common(password):
    common_passwords = ["PASSWORD", "PASSWORDS", "QWERTYS", "QWERTY"]
    common = False
    password_nonumbers = ''.join([i for i in password if not i.isdigit()])
    password_nonumbers = password_nonumbers.upper()

    print(password_nonumbers)
    for word in common_passwords :
        if word in password_nonumbers:
            common = True
    return common
#Validation end

if __name__ != '__main__':
    Scheduler.StartSoup()