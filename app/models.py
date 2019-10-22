#!/usr/bin.env python3
"""
This file contains database models for the application
"""
from app import db

class User(db.Model):
    """
    This class defines the User
    object to represent a particular
    user for the application
    """
    id = db.Column(db.integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f"Uers <{self.username}>"
