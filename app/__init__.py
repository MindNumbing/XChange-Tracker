from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)

app.config.from_object('config')

login_manager = LoginManager(app)

from app.auth.views import auth_view
from app.admin import admin_view

app.register_blueprint(auth_view)
app.register_blueprint(admin_view)

from app.database.db import db_session
from app import database
from app import views
from app import scheduler
