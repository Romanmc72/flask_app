#!/usr/bin/env python3
"""
Here we initialize the flask application. When this directory is
initialized via import from the file outside of this directory,
it will instantiate the application and begin with routing the
user to various web pages.
"""
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)

from app import routes
from app import models
from app import forms
from app import errors
