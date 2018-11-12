from flask import (
    render_template,
    Flask
)

# Import Migrate
from flask_migrate import Migrate

# Import CORS
from flask_cors import CORS

# import application configuration
import config

"""
Initialize the flask application
Appropriately name the application
Read application config from config.py
"""
app = Flask('feature_requests')

with app.app_context():
    app.config.from_object(config)

    from . import models, forms

    # initialize migrate to manage db migrations
    migrate = Migrate(app, models.db)

    # initialize cors
    CORS(app)

    from .views import *