from flask import render_template, session
from app import app
from app.database.db import db_session
from app.database.functions import get_data
from flask_login import current_user


@app.route('/')
@app.route('/index')
def index():
    session['User'] = ''
    return render_template('index.html', Data=get_data())


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
