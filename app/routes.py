#!/usr/bin/env python3
"""
This file contains the various routes to
different pages on the Flask site,
and how those html templates are populated.
"""
from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    # TODO DOCUMENT ME
    """
    form = LoginForm()
    if form.validate_on_submit():
        flash(f"Login requested for {form.username.data}, remember me = {form.remember_me.data}")
        return redirect(url_for('index'))
    return render_template("login.html", title='Login', form=form)
