#!/usr/bin.env python3
"""
This file contains database models for the application
"""
import os

from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from app import db
from app import login

DEFAULT_SCHEMA = {"schema": os.getenv('DEFAULT_SCHEMA', 'flask_app')}


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
