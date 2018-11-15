"""
flask application initialization module
"""
from . import factories

app = factories.create_app()

with app.app_context():

    # import custom commands
    from . import commands
