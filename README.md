# Feature Request Web Application
A web application that allows the user to create "feature requests". A "feature request" is a request for a new feature that will be added onto an existing piece of software. 

## Installing / Getting started

Here's a quick introduction of the minimal setup you need to get the feature requests web application up & running.

#### Prerequisites

Here are the things you need to setup the application
 - python3.6 
 - virtualenv ( to setup virtual environment )
 - postgresql ( database )
 - Linux OS

### Initial Configuration

 #### Environment Variables
 
You need to run the following to temporarily set the environment variables
```bash
export POSTGRES_HOST='postgres'
export POSTGRES_PASS='postgres'
export POSTGRES_USER='localhost'
export POSTGRES_DATABASE='feature_requests'
export POSTGRES_TEST_DATABASE='test_feature_requests'
export FLASK_ENV='development'
```
**or to permanently set the environment variables**
```bash
echo "export POSTGRES_HOST='postgres'
export POSTGRES_PASS='postgres'
export POSTGRES_USER='localhost'
export POSTGRES_DATABASE='feature_requests'
export POSTGRES_TEST_DATABASE='test_feature_requests'
export FLASK_ENV='development'" > ~/.bashrc
```
**Note:** change values above to match your postgresql instance

### Setup Application
 
```shell
git clone https://github.com/stikks/Feature-Request.git
cd Feature-Request

# run setup bash script
bash setup.sh
```

**To run in development mode**
```shell
export FLASK_ENV='development'
```

**for production mode** 

```shell
export FLASK_ENV='production'
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
 

## Running tests

The tests are run using pytest. The test cases are in the directories application/tests and application/core/tests

```bash
pytest
```

These tests all the defined routes for the application and service methods for each model defined in the application.

### Building Application

To build application, run

```shell
pip install -e .
```

### Running Application

```shell
flask run

visit http://localhost:5000 to view application
```

#### Accessing Application
Demo credentials for accessing the application
```pydocstring
username - ada@iws.com
password - lovelace
```

## Deployment

This describes the deployment process on an Ubuntu Cloud VPS. 

#### Prerequisites
You need a server running on 

> Ubuntu OS >= 14.04

with the following services installed 

> Gunicorn

> Nginx

Fabric is needed for the deployment
```bash
pip install Fabric==1.14.0
```

Before we begin, you need to set the environment variable for the server url
```bash
export SERVER_DEPLOYMENT_URL='root@127.0.0.1'
```

**replace 'root' and '127.0.0.1' with appropriate information**

With Fabric, we can create scripts to deploy the application to the server. (**fabfile.py**)

To run the deployment,
```bash
fab deploy
```

The command above creates an ssh connection to url defined in environment variable **SERVER_DEPLOYMENT_URL**
and deploys the application. 

The application runs on port **8045**

**If the server is behind a firewall, expose port 8045**

## Built With

[Flask](http://flask.pocoo.org/) - Web framework used

[Bootstrap](https://getbootstrap.com/) 


## Contributing

If you'd like to contribute, please fork the repository and use a feature
branch. Pull requests are warmly welcome.


## Links

- Project homepage: https://github.com/stikks/Feature-Request
- Repository: https://github.com/stikks/Feature-Request.git
- Issue tracker: https://github.com/stikks/Feature-Request/issues
  - In case of sensitive bugs like security vulnerabilities, please contact
    oladipoqudus@gmail.com directly instead of using issue tracker. We value your effort
    to improve the security and privacy of this project!

## Licensing

The code in this project is licensed under MIT license.