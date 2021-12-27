#!/bin/bash

BASEDIR=`dirname $0` 
echo $BASEDIR
cd $BASEDIR
cd src

source ../bin/activate
export FLASKR_SETTINGS='./config.py'
while true
do
  ./flaskr.py 
  sleep 10
done
deactivate

