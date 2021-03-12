#!/usr/bin/env python3
"""
This file contains the various routes to
different pages on the Flask site,
and how those html templates are populated.
"""
from time import time
import json
import base64

from flask import abort
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
from app import db
from app.email import send_password_reset_email
from app.forms import GarageDoorApp
from app.forms import LoginForm
from app.forms import NewLoginForm
from app.forms import PasswordResetRequestForm
from app.forms import PasswordResetForm
from app.models import User
from app.models import Score
from app.remote_control import open_garage_door
from app.remote_control import refresh_garage_door_picture


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
        footer="If you don't have a profile click I am new here or if you forgot your password then click that link."
    )


@app.route('/new_login', methods=['GET', 'POST'])
def new_login():
    """
    Description
    -----------
    This function opens up a new user log
    in page for users who have not previously
    logged into the app

    Params
    ------
    None

    Return
    ------
    Returns a rendered Jinja2 HTML template served
    over the flask application under the
    `/new_login' path
    """

    # If a user that is already logged in
    # somehow gets here, they'll get sent
    # back to the home page
    if current_user.is_authenticated:
        redirect(url_for('index'))

    # Upon submission of the form,
    # everything should be validated,
    # once that is done, if all things
    # pass validly then the user will
    # be sent to the next page home page
    form = NewLoginForm()
    if form.validate_on_submit():

        # Just make sure they don't already exist
        # via either the email or the username
        user = User.query.filter_by(username=form.username.data).first()
        email = User.query.filter_by(email=form.email.data.lower()).first()
        if not user and not email:

            # Instantiate the new user and add them to the database
            new_user = User(username=form.username.data, email=form.email.data.lower())
            new_user.set_password(form.password.data)
            new_user.role = 'user'
            new_user.created_at = time()
            new_user.last_modified_at = new_user.created_at
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)

            # Then return to the home page.
            return redirect(url_for('index'))
        elif user and email:
            form.username.errors.append('This username already exists')
            form.email.errors.append('This email already exists')
        elif user:
            form.username.errors.append('This username already exists')
        elif email:
            form.email.errors.append('This email already exists')

    return render_template('new_login.html', title='New kid alert!', form=form, footer='Welcome new person.')


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


@app.route('/super_user/<username>', methods=['GET', 'POST'])
@login_required
def super_user(username: str) -> render_template:
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
    `/super_user/<username>' path, depending on the username
    """
    user = User.query.filter_by(username=username).first_or_404()
    if user.role == 'admin':
        form = GarageDoorApp()

        if form.validate_on_submit():
            if form.open_garage_door.data:
                flash("[ Running the garage door app, give it a second... ]")
                details = open_garage_door(current_app)
                for detail in details:
                    flash(detail)

            if form.status_picture.data:
                flash("[ Refreshing the picture, this will take a second... ]")
                refresh_garage_door_picture(current_app)

        return render_template('super_user.html', user=user, form=form, ts=int(time()))
    else:
        abort(403)


@app.route('/user/<username>', methods=['GET'])
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
    scores = Score.get_user_best_scores(username=current_user.username)
    stats = Score.get_user_stats(username=current_user.username)
    return render_template(
        'user.html',
        header="Welcome!",
        user=current_user,
        scores=scores,
        stats=stats,
        footer="Thanks for logging in <3"
    )


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    """
    Description
    -----------
    This function takes the user to the web page
    where they can initiate a password reset request.
    Params
    ------
    None
    Return
    ------
    Returns a rendered Jinja2 HTML template served
    over the flask application under the
    `/reset_password/<token>' path
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            send_password_reset_email(user)
            flash('A password reset has been sent to that email if a profile exists.')
        return redirect(url_for('login'))
    return render_template(
        'reset_password_request.html',
        form=form,
        header='Well get on it then!',
        footer='Once you submit there will only be 10 minutes to reset you password. Good Luck!'
    )


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """
    Description
    -----------
    This function takes a token and returns the specific password
    reset page for a particular user if they have forgotten or
    lost their password.
    Params
    ------
    :token: str
    The string representation of a JSON web token.
    Return
    ------
    Returns a rendered Jinja2 HTML template served
    over the flask application under the
    `/reset_password/<token>' path
    """
    reroute = redirect(url_for('index'))
    if current_user.is_authenticated:
        return reroute
    user = User.verify_password_reset_token(token)
    if not user:
        return reroute
    form = PasswordResetForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        user.last_modified_at = time()
        db.session.commit()
        flash('Your password has been successfully reset.')
        return redirect(url_for('login'))
    return render_template(
        'reset_password.html',
        form=form,
        header='Pick a new password since you forgot the other one.',
        footer='We all forget sometimes.'
    )

@app.route('/game')
def game():
    """Returns the webpage for the javascript based game."""
    if not current_user.is_authenticated:
        username = None
    else:
        username = current_user.username

    now = time()
    score = Score(username=username, score=0, token_used=False, created_at=now, last_modified_at=now)
    score.save()

    game_token = score.issue_web_token()

    top_scores = Score.get_best_scores()

    return render_template(
        'game.html',
        header=f"Try and beat the high score!",
        token=game_token,
        footer='I made this game using the <a href="https://phaser.io/tutorials/making-your-first-phaser-3-game/part1">PhaserJS</a> tutorial.',
        hostname=current_app.config['HOSTNAME'],
        scores=top_scores
    )


@app.route('/api/game/score/<game_token>', methods=['POST'])
def api_game_score(game_token):
    """Post a score from the game once the game is over to this endpoint to save it"""


    def check_score(score, game_start_timestamp):
        """
        Checks to see if a given score is even feasible.
        Given it takes 5 seconds to go across the stage left-to-right and
        there are 120 points available per stage crossing attempt. We know
        when you started playing as well as what time it is now so we can
        calculate if your score is even feasible.
        """
        seconds_to_cross_stage = 5
        points_per_coin = 10
        points_per_stage_cross = 12 * points_per_coin
        seconds_elapsed = time() - float(game_start_timestamp)
        practical_maximum = (seconds_elapsed / seconds_to_cross_stage) * points_per_stage_cross
        if score > practical_maximum or score % points_per_coin != 0:
            return False
        else:
            return True

    try:
        token, score_str = base64.standard_b64decode(game_token).decode('utf-8').split(',')
        score = int(score_str)
    except ValueError:
        abort(400)

    game_instance = Score.verify_web_token(token)

    if not game_instance:
        abort(400)

    valid_score = check_score(score, game_instance.created_at)

    if game_instance.token_used or not valid_score:
        return Response(
            json.dumps({'text': 'Permission Denied, score not updated.', 'score': score}),
            status=403,
            mimetype='application/json'
        )
    else:
        game_score = int(score)
        game_instance.update(score=game_score, token_used=True, last_modified_at=time())
        return Response(
            json.dumps({'text': 'Score updated', 'score': game_score}),
            status=200,
            mimetype="application/json"
        )
