from flask import Flask, render_template
from flask_login import LoginManager

from app.scheduler import Scheduler

# Import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Define login manager
login_manager = LoginManager(app)

#Blueprint registration stuff
# Import a module / component using its blueprint handler variable (mod_auth)
from app.auth.views import auth as auth_module
from app.admin.views import adminBlueprint as admin_module

# Register blueprint(s)
app.register_blueprint(auth_module)
app.register_blueprint(admin_module)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
from app.database.db import init_db
init_db()

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from app.database.db import db_session

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

from app import views