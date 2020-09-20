#!/usr/bin/env python3
"""
Connects via SSH to the desired client and runs the command passed in
"""
import paramiko


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
        # print("Output: {output_text}".format(output_text=stdout.read().decode()))
        # print("Error: {error_text}".format(error_text=stderr.read().decode()))
    finally:
        client.close()
    return [stdout.read().decode(), stderr.read().decode()]
