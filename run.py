#!flask/bin/python
from app import app

import logging

logging.basicConfig(level=logging.DEBUG)

app.run(debug=True)

