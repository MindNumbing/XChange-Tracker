from flask_login import login_user, logout_user, login_required, current_user
from flask import Blueprint, request, render_template, session, redirect, url_for, flash
from app import login_manager
from app.soup import soup
from app.database.db import db_session
from app.database.functions import get_hash, get_data, verify_password
from app.database.model import File
from app.auth.model import User
from app.auth.forms import LoginForm
from datetime import datetime

auth_view = Blueprint('auth', __name__, url_prefix='/auth')


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


@auth_view.route('/')
@auth_view.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if current_user.is_authenticated is False:
        if request.method == 'POST' and form.validate():
            user = db_session.query(User).filter_by(username=form.username.data).first()
            valid_password = verify_password(user.username, form.password.data)
            if user:
                if valid_password:
                    login_user(user)
                    if user.permission:
                        session['User'] = 'Admin'
                        flash('You are logged in as an Admin', 'success')
                    else:
                        session['User'] = 'User'
                        flash('You are logged in as a User', 'success')
            return redirect(url_for('auth.auth_index'))
    else:
        flash('You are already logged in', 'info')
        return redirect(url_for('auth.auth_index'))
    return render_template('auth/login.html', form=form)


@auth_view.route('/logout', methods=['POST'])
@login_required
def logout():
    flash('You have been logged out successfully', 'success')
    logout_user()
    return redirect(url_for('index'))


@auth_view.route('/index', methods=['GET'])
@login_required
def auth_index():
    return render_template('auth/index.html', Data=get_data())


@auth_view.route('/scrape', methods=['POST', 'GET'])
@login_required
def scrape():
    name = request.form['name']
    website = request.form['webpage']

    flash('The website has been scraped, please find your files below', 'success')

    files = soup.make_soup(website)
    if files is not None:
        for file in files:
            result = db_session.query(File).filter_by(file_address=file).first()
            if result is None:
                temp = File(website=name, file_address=file, date=datetime.now(), hash=get_hash(file))
                db_session.add(temp)
                db_session.commit()
    return redirect(url_for('auth.auth_index'))
