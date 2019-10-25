#!/usr/bin/env bash

FLASK_APP=./flask_app.py

function db.up() {
    pushd $REPO/My_Dockerfiles/db/postgres/
    ./up.sh
    popd
}

function db.down() {
    pushd $REPO/My_Dockerfiles/db/postgres/
    ./down.sh
    popd
}

function db.init() {
    echo "Setting up ${FLASK_APP} as the Flask App"
    echo "Entering virtual environment"
    source venv/bin/activate
    echo "Running the db init command"
    flask db init || flask db migrate
    echo "
    bye!"
}

function db.upgrade() {
    echo "Upgrading db for ${FLASK_APP}"
    flask db upgrade
    echo "bye!"
}

function db.downgrade() {
    echo "Downgrading db for ${FLASK_APP}"
    flask db downgrade
    echo "bye!"
}

function flask.run() {
    FLASK_APP=./flask_app.py
    echo "Setting up ${FLASK_APP} as the Flask App"
    echo "Entering virtual environment"
    source venv/bin/activate
    echo "Opening localhost"
    open http://localhost:5000
    echo "Running ${FLASK_APP}, Press control+C to exit."
    flask run
    echo "
    bye!"
}

function flask.deploy() {
    echo 'Shelling into remote server and pulling down repository.'
    ssh pi@$(nslookup r0m4n.hopto.org | grep -v '#' | awk '/Address/ { print $2 }') 'bash -s' < _pull_down_master.sh
    echo 'All Done!'
    echo 'Exited, Goodbye!'
}

function flask.tutorial() {
    echo "Opening the tutorial in your browser"
    open https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
}
