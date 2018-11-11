![Logo of the project](https://github.com/stikks/Feature-Request/blob/master/logo.png)

# Feature Request Web Application
> Additional information or tagline

A web application that allows the user to create "feature requests". A "feature request" is a request for a new feature that will be added onto an existing piece of software. 

## Installing / Getting started

A quick introduction of the minimal setup you need to get the feature requests web application up & running.

This app was built using Flask microframework, you can find the list of dependencies in the requirements.txt file

```shell
flask run

visit http://localhost:5000 to view application
```

### Initial Configuration

## Developing

Here's a brief intro about what a developer must do in order to start developing
the project further on a Linux machine:

To setup the application, you need to have the following installed
 - python ( preferably python3 )
 - virtualenv ( to setup virtual environment )
 - postgresql ( database )

```shell
git clone https://github.com/stikks/Feature-Request.git
cd Feature-Request

# create a virtual environment
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt

## setting up database connection
psql -U {username} -h {host} -c "create database {db name}"

## postgresql configuration
default postgresql connection URI
 - SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost/feature_requests"
   - "postgresql://{username}:{password}@{host}/{db name}"

 change value in "config.py" to match

# initialize migrations
flask db init
flask db migrate
flask db upgrade

flask run
```

### Building Executable

To build executable ( on linux )

```shell
pyinstaller -w -F --add-data "app:app" --add-data "migrations:migrations" --add-data "templates:templates" --add-data "static:static" -p /home/stikks/Documents/projects/Interview_Calendar/venv/lib/python3.5/site-packages setup.py

# run executable using
./dist/setup

visit http://localhost:5055 to view application
```

## Configuration

If you want to run the app in development mode, run
```shell
export FLASK_ENV='development'
```
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