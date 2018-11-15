"""
flask application factory module
"""

from logging.handlers import RotatingFileHandler

from flask import Flask, logging as flask_logging

# import application configuration
import config


def register_blueprints(app: Flask):
    """
    register app blueprints
    :param app
    :return:
    """
    # import all routes
    from application.core import core

    app.register_blueprint(core)


def initialize_extensions(app: Flask):
    """
    initialize flask app extensions
    :param app:
    :return:
    """
    # import login manager
    from flask_login import LoginManager

    # Import Migrate
    from flask_migrate import Migrate

    # import sqlalchemy
    from flask_sqlalchemy import SQLAlchemy

    # Import bcrypt
    from flask_bcrypt import Bcrypt

    # import flask marshmallow
    from flask_marshmallow import Marshmallow

    # import database
    from .database import db

    # Define database object
    db.init_app(app)
    app.db = db

    # initialize migrate to manage db migrations
    Migrate(app, db)

    # add a rotating file handler
    handler = RotatingFileHandler('feature_requests.log', maxBytes=15000, backupCount=2)
    app.logger.addHandler(handler)

    # remove default logging handler
    app.logger.removeHandler(flask_logging.default_handler)

    # initialize flask login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "core.login"
    app.login_manager = login_manager

    # setup bcrypt for encrypting password
    bcrypt = Bcrypt(app)
    app.bcrypt = bcrypt

    # initialize marshmallow for serialization
    marshmallow = Marshmallow(app)
    app.marshmallow = marshmallow

    return app


def create_app(app_name='feature_requests', app_config=config.BaseConfig):
    """
    create flask app

    register blueprints and initialize
    extensions
    :return:
    """
    """
    Initialize the flask application
    Appropriately name the application
    Read application config from config.py
    """
    app = Flask(app_name)

    with app.app_context():
        app.config.from_object(app_config)

        initialize_extensions(app)

        register_blueprints(app)

    return app

