#!/usr/bin/env python3
"""
This file defines the form used for logging into the site
"""
import textwrap

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import Regexp
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import Length

class LoginForm(FlaskForm):
    """
    Description
    -----------
    This class defines the form that gets called whenever a user logs into the site.

    The login form object renders various fields in the html templates as they're
    defined here below. The objects below are accessible elements of a form instance.

    So you can instantiate this form when a route is accessed, render the fields
    described below, and access the data later on in the site.

    Params
    ------
    None
    
    Methods
    -------
    Inherits methods from `flask_wtf.FlaskForm'
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class NewLoginForm(FlaskForm):
    """
    Description
    -----------
    This class defines the form that gets called whenever a user logs into the
    site for the first time.

    The login form object renders various fields in the html templates as they're
    defined here below. The objects below are accessible elements of a form instance.

    So you can instantiate this form when a route is accessed, render the fields
    described below, and access the data later on in the site.

    Params
    ------
    None
    
    Methods
    -------
    Inherits methods from `flask_wtf.FlaskForm'
    """
    password_must_contain = textwrap.dedent("""
    Password must contain:
    1 capital letter 'A-Z',
    1 lowercase letter 'a-z',
    1 number '0-9',
    and 1 special character in the set '`~!@#$%^&()_+={}[]|\\?:;>.<,\"\'-*/'.
    """)
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                regex=r"[a-z0-9_]{6,64}",
                message="Use between 6 and 64 lowercase letters 'a-z', numbers '0-9', or underscores '_'"
            )
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Regexp(r".*[A-Z].*", message=password_must_contain + " missing capital letter"),
            Regexp(r".*[a-z].*", message=password_must_contain + " missing lowercase letter"),
            Regexp(r".*[0-9].*", message=password_must_contain + " missing number"),
            Regexp(r".*[`~!@#$%^&()_+={}\[\]|\\?:;>.<,\'\"\-\*\/].*", message=password_must_contain + " missing special character"),
            Length(min=8, max=128, message="Please enter a password between 8 and 128 characters")
        ]
    )
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="Confirm Password must match Password")])
    email = StringField('Email', validators=[DataRequired(), Email(message=u"That does not look like an email \U0001F622")])
    submit = SubmitField('Submit')
