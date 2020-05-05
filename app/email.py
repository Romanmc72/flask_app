#!/usr/bin/env python3
"""
This file exists to handle any outbound emails from this application to the users of the applicaction
"""
from threading import Thread

from flask import render_template
from flask_mail import Message

from app import app
from app import mail


def send_async_email(app, msg) -> None:
    """
    Description
    -----------
    This function takes in the flask application and an email message then starts
    another context of this application under which the email will be sent. This
    will allow the current application to proceed on the thread it is running
    through without seeing a decrease in speed while the email is being sent.

    Params
    ------
    :app:
    The Flask application object found in `from app import app` or app.app.

    :msg:
    A flask mail email message that is to be sent

    Return
    ------
    None
    """
    with app.app_context():
        mail.send(msg)


def compose_email_message(
    subject: str,
    sender: str,
    recipients: list,
    text_body: str = None,
    html_body: str = None
):
    """
    Description
    -----------
    This method lets me compose a flask mail message without needing to send it,
    so that there is a uniform way to compse the message without forcing me also
    to send the message in the same function and the same way every time.

    Params
    ------
    :subject: str
    The subject line for the email

    :sender: str
    Who the email will appear to be from

    :recipients: list
    The person intended to receive the email

    :text_body: str = None
    The text body for the email,
    if you wish to send with a text based body.

    :html_body: str = None
    The html body for the email,
    if you wish to send with an html based body

    Return
    ------
    The message object for flask mail.
    """


def send_email(
    subject: str,
    sender: str,
    recipients: list,
    text_body: str = None,
    html_body: str = None
) -> None:
    """
    Description
    -----------
    This function sends an email with the provided
    subject line from the provided sender to the
    provided recipient(s) containing the text and
    or html body.

    You must provide at least one text/html body.
    A body-less email will raise an error.

    Params
    ------
    :subject: str
    The subject line for the email

    :sender: str
    Who the email will appear to be from

    :recipients: list
    The person intended to receive the email

    :text_body: str = None
    The text body for the email,
    if you wish to send with a text based body.

    :html_body: str = None
    The html body for the email,
    if you wish to send with an html based body

    Return
    ------
    None
    This function does not return anything,
    it simply sends an email according to
    what is passed in.
    """
    if text_body is None and html_body is None:
        raise ValueError("You have no text or html body. Please provide one of the two. You cannot send a body-less email.")
    msg = Message(subject, sender=sender, recipients=recipients)

    if text_body:
        msg.body = text_body

    if html_body:
        msg.html = html_body

    Thread(
        target=send_async_email,
        kwargs={
            "app": app,
            "msg": msg
        }
    ).start()


def send_password_reset_email(user) -> None:
    """
    Description
    -----------
    This function takes a particular user and send the password
    reset for that users email to their email address according
    to the database.

    Params
    ------
    :user:
    The flask app.modesl.User class instance of a user.

    Return
    ------
    None
    This jsut sends an email.
    """
    token = user.get_password_reset_token()
    send_email(
        subject="Password Reset Request",
        sender=app.config['ADMINS'][0],
        recipients=[user.email],
        html_body=render_template(
            'email/reset_password.html',
            user=user,
            token=token
        )
    )
