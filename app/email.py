#!/usr/bin/env python3
"""
This file exists to handle any outbound emails from this application to the users of the applicaction
"""
from flask_mail import Message
from app import mail

def send_email(
    subject: str,
    sender: str,
    recipients: list,
    text_body: str = None,
    html_body: str = None) -> None:
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

    mail.send(msg)
