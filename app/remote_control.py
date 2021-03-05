#!/usr/bin/env python3
"""
Connects via SSH to the desired client and runs the command passed in
"""
import os
import base64

from flask import url_for
import paramiko


def open_garage_door(current_app):
    """Runs the remote control command to open the garage door"""
    return execute_remote_command(
        command="python2 /usr/src/RPiGPIO/app/garage_door.py --pin=14",
        username=current_app.config['GARAGE_DOOR_USERNAME'],
        password=current_app.config['GARAGE_DOOR_PASSWORD'],
        hostname=current_app.config['GARAGE_DOOR_HOSTNAME']
    )


def refresh_garage_door_picture(current_app):
    """Runs the remote control command to take a picture of the garage door."""
    picture_text = execute_remote_command(
        command="python3 /usr/src/RPiGPIO/app/capture_and_send_image.py",
        username=current_app.config['GARAGE_DOOR_USERNAME'],
        password=current_app.config['GARAGE_DOOR_PASSWORD'],
        hostname=current_app.config['GARAGE_DOOR_HOSTNAME']
    )[0]
    picture_binary = base64.standard_b64decode(picture_text.encode('utf-8'))

    # Finds the absolute location of this file on disk regardless of which
    # system you're using.
    file_location = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        url_for('static', filename='garage/status.jpg')[1::]
    )

    with open(file_location, 'wb') as picture_file:
        picture_file.write(picture_binary)


def execute_remote_command(command: str,
                           username: str,
                           hostname: str,
                           password: str) -> None:
    """
    Description
    -----------
    This function submits the command to desired host in order to run under
    the authenticated context you give it.

    Params
    ------
    :command: str
    The command to be executed on the remote machine.

    :username: str
    The username to log into the remote machine as.

    :hostname: str
    The hostname (IP or DNS name) for the remote machine.

    :password: str
    The password used to log in with.

    Return
    ------
    None
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname, username=username, password=password)
    try:
        stdin, stdout, stderr = client.exec_command(command)
        output = [stdout.read().decode(), stderr.read().decode()]
        # print("Output: {output_text}".format(output_text=stdout.read().decode()))
        # print("Error: {error_text}".format(error_text=stderr.read().decode()))
    finally:
        client.close()
    return output
