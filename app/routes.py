#!/usr/bin/env python3
"""
This file contains the various routes to
different pages on the Flask site,
and how those html templates are populated.
"""
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from werkzeug.urls import url_parse

from app import app
from app.forms import LoginForm
from app.models import User


@app.route('/')
@app.route('/index')
@login_required
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
    list_of_things = [
        'What is new at work?',
        'What are you doing in Docker?',
        'What was the last thing you coded for fun?',
        'What other non-coding things do I do with my computer?',
    ]
    return render_template(
        'index.html',
        list_of_things=list_of_things
    )


@app.route('/login', methods=['GET', 'POST'])
def login() -> render_template:
    """
    Description
    -----------
    This function routes the user either to the
    login page or to the root/index page if the
    user logs in or is logged in

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
        
        # If the user was directed to the login from another page,
        # this will either retun them to page that they came from
        # or will default them back to /index
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    # Otherwise stay here on the login page
    # and wait for the form submission
    return render_template("login.html", title='Login', form=form)


@app.route('/logout')
def logout():
    """
    Description
    -----------
    This function takes the user to the logout page
    and removes

    Params
    ------
    None

    Return
    ------
    logs a user out and then returns a rendered
    Jinja2 HTML template to be served
    over the flask application under the `/index' path
    """
    logout_user()
    return redirect(url_for('index'))
