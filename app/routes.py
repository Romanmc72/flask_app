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
from flask_login import current_user
from flask_login import login_user

from app import app
from app.forms import LoginForm
from app.models import User

@app.route('/')
@app.route('/index')
def index() -> render_template:
    """
    Description
    -----------
    This function defines the root `/'
    and `/index' route for the website

    Params
    ------
    None

    Return
    ------
    returns a rendered Jinja2 HTML template to be served
    over the flask application under the `/index' or `/' path
    """
    user = current_user
    list_of_things = [
        'What is new at work?',
        'What are you doing in Docker?',
        'What was the last thing you coded for fun?',
        'What other non-coding things do I do with my computer?',
    ]
    return render_template(
        'index.html',
        title=f"Welcome {user.username.data}",
        list_of_things=list_of_things
    )

@app.route('/login', methods=['GET', 'POST'])
def login() -> render_template:
    """
    Description
    -----------

    Params
    ------
    None

    Return
    ------
    returns a rendered Jinja2 HTML template to be served
    over the flask application under the `/login' path
    """

    # flask_login stores the concept of a current user
    # if the user is logged in, this will redirect to
    # the home page
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # If the user is not logged in then the flask
    # application will begin the login and
    # authenitcation process
    form = LoginForm()
    if form.validate_on_submit():

        # This returns the user for the form submission if one exists
        # Otherwise returns None
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            
            # Go back to login if no user or wrong password
            flash("[ Invalid Username Or Passowrd ]")
            return redirect(url_for('login'))

        # If login succeeds
        # (user is non None and password is not invalid)
        # go back to home page
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))

    # Otherwise stay here on the login page
    # and wait for the form submission
    return render_template("login.html", title='Login', form=form)
