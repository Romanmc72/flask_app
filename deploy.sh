#!/usr/bin/env bash

echo 'Shelling into remote server'
ssh pi@$(nslookup r0m4n.hopto.org | grep -v '#' | awk '/Address/ { print $2 }')
echo 'Repositioning to Flask Application repository'
cd /var/www/flask_app
echo 'Pulling down master branch updates'
git pull
echo 'All Done!'
echo 'Exiting, Goodbye!'
exit
echo 'All Done!'
echo 'Exited, Goodbye!'
