import timeit
from multiprocessing import cpu_count
from multiprocessing.dummy import Pool as ThreadPool
from flask import render_template, redirect, request, session
from app import app
from app.database.db import db_session
from app.database.functions import GetData
from flask_security import current_user
from app.auth.model import User

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
@app.route('/index')
def index():
    session['User'] = ''
    return render_template('index.html', Data=GetData())

@app.route('/404', methods=['GET'])
def page_not_found():
    return render_template('404.html')