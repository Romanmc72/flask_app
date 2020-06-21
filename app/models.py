#!/usr/bin.env python3
"""
This file contains database models for the application
"""
import os
from time import time

import jwt
from jwt.exceptions import DecodeError
from jwt.exceptions import InvalidTokenError
from jwt.exceptions import InvalidSignatureError
from jwt.exceptions import ExpiredSignatureError
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from app import app
from app import db
from app import login

DEFAULT_SCHEMA = {"schema": os.getenv('DEFAULT_SCHEMA', 'flask_app')}
TOKEN_EXPIRE = 600
ALGORITHM = 'HS256'


class User(UserMixin, db.Model):
    """
    Description
    -----------
    This class defines the User
    object to represent a particular
    user for the application and will be
    stored in the database associated
    with the flask application
    """
    __table_args__ = DEFAULT_SCHEMA
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self) -> str:
        """Returns a string representation of the User"""
        return f"User <{self.username}>"

    def set_password(self, password: str) -> None:
        """
        Description
        -----------
        This function sets a password hash based on the password input

        Params
        ------
        :password: str
        A password to be hashed, this hashed password will be assigned
        to self.password_hash for the current user

        Return
        ------
        None
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Description
        -----------
        This function checks a password against the password hash stored in the database

        Params
        ------
        :password: str
        The password checked against the particular user

        Return
        ------
        bool
        Whether or not the provided password matches the password hash
        """
        return check_password_hash(self.password_hash, password)

    def get_password_reset_token(self, expires_in: int = TOKEN_EXPIRE) -> str:
        """
        Description
        -----------
        This function takes the user's ID, the application's secret key and the token expiration
        time and returns a string representation of the token which can be used externally to
        validate a user's identity and reset their password.

        Params
        ------
        :expires_in: int
        The number of seconds that the json web token will be active for before it expires.

        Return
        ------
        str
        The string representation of the json web token.
        """
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'],
            algorithm=ALGORITHM
        ).decode('utf-8')

    @staticmethod
    def verify_password_reset_token(token: str):
        """
        Description
        -----------
        This function takes in a json web token and either
        outputs the associated user or returns None.

        Params
        ------
        :token: str
        The json web token in string form.

        Return
        ------
        The user associated to the user id.
        """
        try:
            id = jwt.decode(
                token,
                app.config['SECRET_KEY'],
                algorithms=[ALGORITHM]
            )['reset_password']
        except DecodeError or InvalidTokenError or InvalidSignatureError or ExpiredSignatureError:
            return None
        return User.query.get(id)


@login.user_loader
def load_user(id: str) -> User:
    """
    Description
    -----------
    This function loads the user for a particular id

    Params
    ------
    :id: str
    Pass in the id as a string for a given user and this will return that user

    Return
    ------
    User object
    """
    return User.query.get(int(id))
