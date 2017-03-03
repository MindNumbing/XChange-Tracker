from flask_admin import Admin
from app import app
from app.database.db import db_session
from app.auth.model import User
from app.database.model import File
from flask import Blueprint
from app.admin.views import MyIndexView, UserView, FileView

admin_view = Blueprint('admin_view', __name__, url_prefix="/admin")

admin = Admin(app, index_view=MyIndexView(), name='Admin page', template_mode='bootstrap3')
admin.add_view(UserView(User, db_session, endpoint='user'))
admin.add_view(FileView(File, db_session, endpoint='file'))
