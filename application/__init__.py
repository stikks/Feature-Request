from flask import Flask

# import login manager
from flask_login import LoginManager

# Import Migrate
from flask_migrate import Migrate

# Import CORS
from flask_cors import CORS

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

    # initialize migrate to manage db migrations
    from . import models, forms
    migrate = Migrate(app, models.db)

    # # create log file, attach to application
    # from .services import utils
    # app.logger = utils.create_log_file('feature_requests.log')

    # initialize flask login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"
    app.login_manager = login_manager

    # setup bcrypt for encrypting password
    bcrypt = Bcrypt(app)
    app.bcrypt = bcrypt

    # initialize cors
    CORS(app)

    # initialize marshmallow for serialization
    marshmallow = Marshmallow(app)
    app.marshmallow = marshmallow

    # import all routes
    from .views import *

    # import ajax endpoints
    from .ajax_views import *

    # import custom commands
    from .commands import *

