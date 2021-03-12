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
    HOSTNAME = os.getenv('HOSTNAME', 'localhost:5000')
    SECRET_KEY = os.getenv('SECRET_KEY', 'oooh_what_is_it?')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql+psycopg2://flask:not_the_password@0.0.0.0:5432/flask_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'localhost')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 8025))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = [os.getenv('ADMIN_EMAIL', 'admin@r0m4n.com')]
    GARAGE_DOOR_USERNAME = os.environ.get('GARAGE_DOOR_USERNAME', 'root')
    GARAGE_DOOR_PASSWORD = os.environ.get('GARAGE_DOOR_PASSWORD', 'example')
    GARAGE_DOOR_HOSTNAME = os.environ.get('GARAGE_DOOR_HOSTNAME', '0.0.0.0')
