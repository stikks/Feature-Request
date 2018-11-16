![Logo of the project](https://github.com/stikks/Feature-Request/blob/master/static/images/logo.png)

# Feature Request Web Application
> Additional information or tagline

A web application that allows the user to create "feature requests". A "feature request" is a request for a new feature that will be added onto an existing piece of software. 

## Installing / Getting started

A quick introduction of the minimal setup you need to get the feature requests web application up & running.

This app was built using 
Python 3.6.5
Flask micro-framework
Flask extensions

you can find the list of dependencies in the requirements.txt file

```shell
flask run

visit http://localhost:5000 to view application
```

Log on using credentials
> email - ada@iws.com

> password - lovelace

### Initial Configuration

## Developing

Here's a brief intro about what a developer must do in order to start developing
the project further on a Linux machine:

To setup the application, you need to have the following installed
 - python3.6 
 - virtualenv ( to setup virtual environment )
 - postgresql ( database )
 - Linux OS
 
 #### Environment Variables
 
You need to set the following environment variables
> POSTGRES_HOST - postgresql host

> POSTGRES_PASS - postgresql password

> POSTGRES_USER - postgresql user

> POSTGRES_DATABASE - application database

> POSTGRES_TEST_DATABASE - test database
 
```shell
git clone https://github.com/stikks/Feature-Request.git
cd Feature-Request

# run setup bash script
bash setup.sh
```

##### Setup Script

This script makes setting up easier and contains the following commands

```shell
# setup virtual environment
# echo 'setting up virtual environment'
pip3 install -U virtualenv

# activate virtual environment
echo 'activating virtual environment'
virtualenv -p python3 venv
source venv/bin/activate

# install required packages
echo 'installing requirements'
pip3 install -r requirements.txt

# create database
echo 'setup database'
psql -U $POSTGRES_USER -h $POSTGRES_HOST -c "create database $POSTGRES_DATABASE"

# create test database
echo 'setup test database'
psql -U $POSTGRES_USER -h $POSTGRES_HOST -c "create database $POSTGRES_TEST_DATABASE"

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
```
 

### Building Application

To build application, run

```shell
pip install -e .
```

## Configuration

To run the app in development mode, run
```shell
export FLASK_ENV='development'
```

and 
```shell
export FLASK_ENV='production'
```
for production mode


## Contributing

If you'd like to contribute, please fork the repository and use a feature
branch. Pull requests are warmly welcome.

This project using Flask microframework and adopts the PEP8 styling guide

## Links

- Project homepage: https://github.com/stikks/Feature-Request
- Repository: https://github.com/stikks/Feature-Request.git
- Issue tracker: https://github.com/stikks/Feature-Request/issues
  - In case of sensitive bugs like security vulnerabilities, please contact
    oladipoqudus@gmail.com directly instead of using issue tracker. We value your effort
    to improve the security and privacy of this project!

## Licensing

The code in this project is licensed under MIT license.