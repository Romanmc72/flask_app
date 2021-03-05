#!/usr/bin/env python3
"""
This file contains the various routes to
different pages on the Flask site,
and how those html templates are populated.
"""
import json
import base64

from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import current_app
from flask import Response
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from werkzeug.urls import url_parse

from app import app
from app.forms import LoginForm
from app.forms import GarageDoorOpener
from app.models import User
from app.models import Score
from app.remote_control import execute_remote_command


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
    list_of_things = [
        'What is new at work?',
        'What kinds of projects are you working on?',
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
    return render_template(
        "login.html",
        title='Login',
        form=form,
        footer="We are not accepting new applications at this time."
    )


@app.route('/logout')
def logout() -> render_template:
    """
    Description
    -----------
    This function logs the user out
    of the site then redirects them
    to the home page

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


@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username: str) -> render_template:
    """
    Description
    -----------
    This functions takes a user to their
    personal page after having logged in

    Params
    ------
    :username: str
    The username for a given user on the site.

    Return
    ------
    Returns a rendered Jinja2 HTML template served
    over the flask application under the
    `/user/<username>' path, depending on the username
    """
    user = User.query.filter_by(username=username).first_or_404()
    form = GarageDoorOpener()

    if form.validate_on_submit():
        flash("[ Running the garage door, give it a second... ]")
        details = execute_remote_command(
            command="python2 /usr/src/RPiGPIO/app/garage_door.py --pin=14",
            username=current_app.config['GARAGE_DOOR_USERNAME'],
            password=current_app.config['GARAGE_DOOR_PASSWORD'],
            hostname=current_app.config['GARAGE_DOOR_HOSTNAME']
        )
        for detail in details:
            flash(detail)

    return render_template('user.html', user=user, form=form)


@app.route('/game')
def game():
    """Returns the webpage for the javascript based game."""
    if current_user.is_authenticated:
        username = current_user.username
    else:
        username = None

    score = Score(username=username, score=0, token_used=False)
    score.save()
    high_score = score.get_high_score()

    game_token = score.issue_web_token()

    return render_template(
        'game.html',
        header=f"High Score: {high_score}",
        token=game_token,
        footer='I made this game using the <a href="https://phaser.io/tutorials/making-your-first-phaser-3-game/part1">PhaserJS</a> tutorial.'
    )


@app.route('/api/game/score/<game_token>', methods=['POST'])
def api_game_score(game_token):
    """Post a score from the game once the game is over to this endpoint to save it"""
    token, score = base64.standard_b64decode(game_token).decode('utf-8').split(',')
    game_instance = Score.verify_web_token(token)
    if game_instance.token_used:
        return Response(
            json.dumps({'text': 'Permission Denied, score not updated.', 'score': score}),
            status=403,
            mimetype='application/json'
        )
    else:
        game_score = int(score)
        game_instance.update(score=game_score, token_used=True)
        return Response(
            json.dumps({'text': 'Score updated', 'score': game_score}),
            status=200,
            mimetype="application/json"
        )
