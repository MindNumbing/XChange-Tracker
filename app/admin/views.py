from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app import app
from app.database.db import db_session
from app.auth.model import User
from app.database.model import File
from flask import Blueprint


# Define the blueprint: 'auth', set its url prefix: app.url/auth
adminBlueprint = Blueprint('adminPage', __name__, url_prefix='/admin')

#Flask admin initalisation below
admin = Admin(app, name='Admin page', template_mode='bootstrap3')
admin.add_view(ModelView(User, db_session))
admin.add_view(ModelView(File, db_session))
