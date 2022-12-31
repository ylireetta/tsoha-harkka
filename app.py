from os import getenv
from flask import Flask

APP = Flask(__name__)
APP.secret_key = getenv("SECRET_KEY")
APP.templates_auto_reload = True

import routes
