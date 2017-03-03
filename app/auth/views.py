from flask_login import login_user, logout_user, login_required
from flask import Blueprint, request, render_template, session, redirect, url_for
from app import login_manager
from app.soup import soup
from app.database.db import db_session
from app.database.functions import get_hash, get_data, verify_password
from app.database.model import File
from app.auth.model import User
from app.auth.forms import SignupForm, LoginForm
from datetime import datetime

auth_view = Blueprint('auth', __name__, url_prefix='/auth')


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


@auth_view.route('/signupform/', methods=['GET', 'POST'])
def signupform():
    print('signupform')
    return redirect(url_for('auth.signup'))


@auth_view.route('/signup/', methods=['GET', 'POST'])
def signup():
    print('signup')
    form = SignupForm(request.form)

    if form.validate_on_submit():
        if db_session.query(User).filter_by(username=form.username.data).one() is None:
            if db_session.query(User).filter_by(email=form.email.data).one() is None:
                user = User(form.username.data, form.email.data, User(form.password.data))
                db_session.add(user)
                db_session.commit()
                session['user_id'] = user.id
    return render_template("auth/index.html", form=form)


@auth_view.route('/')
@auth_view.route('/login', methods=['GET', 'POST'])
def login():
    print('login')
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = db_session.query(User).filter_by(username=form.username.data).first()
        valid_password = verify_password(user.username, form.password.data)

        if user:
            print('user exists')
            if valid_password:
                print('valid password')
                print('Logging in')
                login_user(user)
                print('logged in')
                print('checking permissions')
                if user.permission:
                    print('admin')
                    session['User'] = 'Admin'
                else:
                    print('user')
                    session['User'] = 'User'
        print('returning to auth index')
        return redirect(url_for('auth.auth_index'))
    print('returning to login')
    return render_template('auth/login.html', form=form)


@auth_view.route('/logout', methods=['POST'])
@login_required
def logout():
    print('logout')
    logout_user()
    return redirect(url_for('index'))


@auth_view.route('/index', methods=['GET'])
@login_required
def auth_index():
    print('index')
    return render_template('auth/index.html', Data=get_data())


@auth_view.route('/scrape', methods=['POST', 'GET'])
@login_required
def scrape():
    print('scrape')
    name = request.form['name']
    website = request.form['webpage']

    files = soup.make_soup(website)
    if files is not None:
        for file in files:
            result = db_session.query(File).filter_by(file_address=file).first()
            if result is None:
                temp = File(website=name, file_address=file, date=datetime.now(), hash=get_hash(file))
                db_session.add(temp)
                db_session.commit()
    return redirect(url_for('auth.auth_index'))
