# Import flask dependencies
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for

from app import login_manager
from flask_login import login_user, logout_user, login_required, current_user

# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash

from app.database.db import db_session

from app import app

# Import module forms
from app.auth.forms import SignupForm, LoginForm

# Import module models (i.e. User)
from app.auth.model import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
auth = Blueprint('auth', __name__, url_prefix='/auth')

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

@auth.route('/signupform/', methods=['GET', 'POST'])
def signupform():
    return redirect(url_for('auth.signup'))

# Set the route and accepted methods
@auth.route('/signup/', methods=['GET', 'POST'])
def signup():

    # If sign in form is submitted
    form = SignupForm(request.form)

    # Verify the sign in form
    if form.validate_on_submit():

        if db_session.query(User).filter_by(username=form.username.data).one() is None:
            if db_session.query(User).filter_by(email=form.email.data).one() is None:
                user = User(form.username.data, form.email.data, generate_password_hash(form.password.data))
                db_session.add(user)
                db_session.commit()
                session['user_id'] = user.id
                flash('Welcome %s' % user.name)

            flash('Email address is already registered', 'error')
        flash('Username is already registered', 'error')

    return render_template("auth/index.html", form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        user = db_session.query(User).filter_by(username=form.username.data).first()
        print(user)
        if user:
            if login_user(user):
                print(current_user.username)
                return redirect(url_for('auth.secret'))
            error = 'Invalid username or password.'
    return render_template('auth/login.html', form=form, error=error)

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@auth.route('/secret', methods=['GET'])
@login_required
def secret():
    return 'This is a secret page. You are logged in as {}'.format(current_user.username)