from os import getenv
from flask_sqlalchemy import SQLAlchemy
from app import APP

APP.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
DB = SQLAlchemy(APP)
