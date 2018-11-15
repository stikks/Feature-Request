"""
custom cli commands
"""
from flask import current_app as app

with app.app_context():

    # import services needed
    from utils import create_dummy_data


    @app.cli.command()
    def setup_app():
        """
        setup application by creating dummy table entries

        create dummy employee account with
        username - ada@iws.com and
        password - lovelace
        :return:
        """
        # create new employee
        return create_dummy_data()
