import timeit
from multiprocessing import cpu_count
from multiprocessing.dummy import Pool as ThreadPool
from flask import render_template, redirect, request, session
from app import app
from app.database.db import db_session

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def start():
    session['error'] = None
    return redirect(request.url_root + 'index', code=302)

@app.route('/index')
def index():

    #TODO GET ALL FILES FROM DATABASE AND PASS THROUGH

    Data={('FileAddress', 'Message')}

    return render_template('index.html', Data=Data)

@app.route('/404', methods=['GET'])
def page_not_found():
    return render_template('404.html')