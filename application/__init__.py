"""
flask application initialization module
"""

from logging.handlers import RotatingFileHandler

from flask import Flask, logging as flask_logging

# import login manager
from flask_login import LoginManager

# Import Migrate
from flask_migrate import Migrate

# import sqlalchemy
from flask_sqlalchemy import SQLAlchemy

# Import bcrypt
from flask_bcrypt import Bcrypt

# import application configuration
import config

# import flask marshmallow
from flask_marshmallow import Marshmallow

"""
Initialize the flask application
Appropriately name the application
Read application config from config.py
"""
app = Flask('feature_requests')

with app.app_context():
    app.config.from_object(config)

    # Define database object
    db = SQLAlchemy()
    db.init_app(app)
    app.db = db

    # initialize migrate to manage db migrations
    migrate = Migrate(app, db)

    # add a rotating file handler
    handler = RotatingFileHandler('feature_requests.log', maxBytes=15000, backupCount=2)
    app.logger.addHandler(handler)

    # remove default logging handler
    app.logger.removeHandler(flask_logging.default_handler)

    # initialize flask login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"
    app.login_manager = login_manager

    # setup bcrypt for encrypting password
    bcrypt = Bcrypt(app)
    app.bcrypt = bcrypt

    # initialize marshmallow for serialization
    marshmallow = Marshmallow(app)
    app.marshmallow = marshmallow

    # import all routes
    from . import views

    # import ajax endpoints
    from . import ajax_views

    # import custom commands
    from . import commands

