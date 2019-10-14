#!/usr/bin/env bash

FLASK_APP=./flask_app.py
echo "Setting up ${FLASK_APP} as the Flask App"
echo "Opening localhost"
open http://localhost:5000
echo "Running ${FLASK_APP}, Press control+C to exit."
flask run
echo "
bye!"