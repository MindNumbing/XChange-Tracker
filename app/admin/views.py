from flask_admin import Admin
from flask import url_for, redirect
from flask_admin.contrib.sqla import ModelView
from app import app
from app.database.db import db_session
from app.auth.model import User
from app.database.model import File
from flask import Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from flask import session
# Define the blueprint: 'auth', set its url prefix: app.url/auth
adminBlueprint = Blueprint('adminPage', __name__, url_prefix="/Admin")

from flask_admin import AdminIndexView, expose
class MyIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        print(session['User'])
        if session['User'] == 'Admin':
            return self.render('admin/index.html')
        return redirect(url_for('index'))

from flask_admin.contrib.sqla import ModelView

class MyModelView(ModelView):
    # Allow only admins to access the Admin views
    def is_accessible(self):
        print(session['User'])
        if session['User'] == 'Admin':
            return True
        return False

#Flask admin initalisation below
admin = Admin(app, index_view=MyIndexView(), name='Admin page', template_mode='bootstrap3')
admin.add_view(MyModelView(User, db_session))
admin.add_view(MyModelView(File, db_session))

