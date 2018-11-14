#!/bin/bash

if [[ -z $POSTGRES_USER && -z $POSTGRES_DATABASE && -z $POSTGRES_HOST ]]; then
    echo 'You need to set environment variables POSTGRES_USER, POSTGRES_HOST and POSTGRES_DATABASE'; exit $ERRCODE;
fi

# setup virtual environment
# echo 'setting up virtual environment'
pip3 install -U virtualenv

# activate virtual environment
echo 'activating virtual environment'
virtualenv venv
source venv/bin/activate

# install required packages
echo 'installing requirements'
pip3 install -r requirements.txt

# create database
echo 'setup database'
psql -U $POSTGRES_USER -h $POSTGRES_HOST -c "create database $POSTGRES_DATABASE"

# set flask environment as development
export FLASK_ENV='development'

# setup migrations and migrate database
echo 'setup migrations and upgrade'
flask db init
flask db migrate 
flask db upgrade

# setup application
flask setup-app

# run application
flask run