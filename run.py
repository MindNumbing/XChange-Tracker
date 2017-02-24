#!flask/bin/python
from app import app
from flask_mail import Mail
import logging

#logging.basicConfig(level=logging.DEBUG)

app.run(debug=False, use_reloader=False)

