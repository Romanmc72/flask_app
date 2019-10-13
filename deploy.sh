#!/usr/bin/env bash

echo 'Shelling into remote server'
ssh pi@$(nslookup r0m4n.hopto.org | grep -v '#' | awk '/Address/ { print $2 }')
echo 'Exiting, Goodbye!'
exit
echo 'Exited, Goodbye!'
