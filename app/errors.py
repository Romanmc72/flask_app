#!/usr/bin/env python3
"""
This python file is to present error message
to our users that are not just the default Flask response.
"""
from flask import render_template

from app import app


@app.errorhandler(400)
def bad_request(error):
    """
    Description
    -----------
    This function brings up the response page for a 400 error.
    """
    return render_template('400.html'), 400


@app.errorhandler(403)
def not_found_error(error):
    """
    Description
    -----------
    This function brings up the response page for a 403 error.
    """
    return render_template('403.html'), 403


@app.errorhandler(404)
def not_found_error(error):
    """
    Description
    -----------
    This function brings up the response page for a 404 error.
    """
    return render_template('404.html'), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """
    Description
    -----------
    This function brings up the response page for a 405 error.
    """
    return render_template('405.html'), 405


@app.errorhandler(500)
def internal_server_error(error):
    """
    Description
    -----------
    This function brings up the response page for a 500 error.
    """
    return render_template('500.html'), 500
