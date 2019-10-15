#!/usr/bin/env python3
"""
This file contains the various routes to
different pages on the Flask site,
and how those html templates are populated.
"""
from flask import render_template
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    """
    # TODO DOCUMENT ME
    """
    user = {'username': 'Miguel'}
    list_of_things = [
        'What is new at work?',
        'What are you doing in Docker?',
        'What was the last thing you coded for fun?',
        'What other non-coding things do I do with my computer?',
    ]
    return render_template(
        'index.html',
        title='Home',
        list_of_things=list_of_things
    )

@app.route('/login')
def login():
    """
    # TODO DOCUMENT ME
    """
    form = LoginForm()
    return render_template("login.html", title='Login', form=form)
