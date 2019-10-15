#!/usr/bin/env python3
"""
Here we initialize the flask application. When this directory is
initialized via import from the file outside of this directory,
it will instantiate the application and begin with routing the
user to various web pages.
"""
from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import routes
