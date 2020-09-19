#!/usr/bin/env python3
"""
This is the application that actually gets run when the CLI calls

$ `flask run`

"""
from app import app
from app import db
from app.models import User


@app.shell_context_processor
def make_shell_context():
    """
    Description
    -----------
    flask can run an interactive shell that will
    pre-import anything specified in this function
    under the alias provided for easy python
    interpreter testing without having to retype
    the same import statements every time.

    Call this by running

    $ `flask shell`

    Params
    ------
    None

    Return
    ------
    None
    """
    return {'db': db, 'User': User}


if __name__ == "__main__":
    app.run(host="0.0.0.0")
