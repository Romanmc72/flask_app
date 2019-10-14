#!/usr/bin/env python3
"""
This is the configuration file which contains
a secret key to protect information in the
back end from attacks on the front.
"""
import os

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'oooh_what_is_it?')
