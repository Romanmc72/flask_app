#!/usr/bin/env python3
"""
This file defines the form used for logging into the site
"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms import SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    """
    # TODO DOCUMENT ME
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
