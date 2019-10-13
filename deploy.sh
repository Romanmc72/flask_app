#!/usr/bin/env bash

echo 'Shelling into remote server and pulling down repository.'
ssh pi@$(nslookup r0m4n.hopto.org | grep -v '#' | awk '/Address/ { print $2 }') 'bash -s' < _pull_down_master.sh
echo 'All Done!'
echo 'Exited, Goodbye!'
