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

PASSWORD_MUST_CONTAIN = textwrap.dedent("""\
    Password must contain:
    1 capital letter 'A-Z',
    1 lowercase letter 'a-z',
    1 number '0-9',
    and 1 special character in the set '`~!@#$%^&()_+={}[]|\\?:;>.<,\"\'-*/'.""")

PASSWORD_VALIDATORS = [
    DataRequired(),
    Regexp(r".*[A-Z].*", message=PASSWORD_MUST_CONTAIN + " missing capital letter"),
    Regexp(r".*[a-z].*", message=PASSWORD_MUST_CONTAIN + " missing lowercase letter"),
    Regexp(r".*[0-9].*", message=PASSWORD_MUST_CONTAIN + " missing number"),
    Regexp(r".*[`~!@#$%^&()_+={}\[\]|\\?:;>.<,\'\"\-\*\/].*", message=PASSWORD_MUST_CONTAIN + " missing special character"),
    Length(min=8, max=128, message="Please enter a password between 8 and 128 characters")
]

# This assumes that the variable for the password
# (to which this confirmation is being compared)
# is named 'password'
CONFRIM_PASSWORD_VALIDATORS = [
    DataRequired(),
    EqualTo(
        'password',
        message="Confirm Password must match Password"
    )
]

EMAIL_VALIDATORS = [DataRequired(), Email(message=u"That does not look like an email \U0001F622")]


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
    password = PasswordField('Password', validators=PASSWORD_VALIDATORS)
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
    password = PasswordField('Password', validators=PASSWORD_VALIDATORS)
    confirm_password = PasswordField('Confirm Password', validators=CONFRIM_PASSWORD_VALIDATORS)
    email = StringField('Email', validators=EMAIL_VALIDATORS)
    submit = SubmitField('Submit')


class PasswordResetRequestForm(FlaskForm):
    """
    Description
    -----------
    Everybody forgets their password sometimes. If the user forgets theirs
    then this form just takes their email address as input and lets the
    password reset page use it to send a password reset email.
    """
    email = StringField('Email', validators=EMAIL_VALIDATORS)
    submit = SubmitField('Submit')


class PasswordResetForm(FlaskForm):
    """
    Description
    -----------
    This form takes and returns the password reset information form the password resest form.
    This will be a validated and unique new password for the user.
    """
    password = PasswordField('Password', validators=PASSWORD_VALIDATORS)
    confirm_password = PasswordField('Confirm Password', validators=CONFRIM_PASSWORD_VALIDATORS)
    submit = SubmitField('Reset My Password')


class GarageDoorApp(FlaskForm):
    """
    Description
    -----------
    This form is simply a submit button for opening and closing my garage door
    at home.
    """
    open_garage_door = BooleanField('Open Garage Door')
    status_picture = BooleanField('Refresh Picture')
    submit = SubmitField('RUN GARAGE DOOR APP!')

