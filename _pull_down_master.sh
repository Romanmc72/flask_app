#!/usr/bin/env bash

echo 'Repositioning to Flask Application repository'
pwd
cd /var/www/flask_app
echo 'Pulling down master branch updates'
git pull
echo 'All Done!'
echo 'Exiting, Goodbye!'
exit
