#!/usr/bin/env python3
"""
This is the configuration file which contains
a secret key to protect information in the
back end from attacks on the front.
"""
import os

# Not sure what this is doing here...
base_dir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    # TODO DOCUMENT ME
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'oooh_what_is_it?')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'postgres://flask:not_the_password@localhost:5432/flask_db')
    SQLALCHEMY_TRACK_MODIFCATION = False
