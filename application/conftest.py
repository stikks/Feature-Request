from sqlalchemy.schema import MetaData, DropConstraint
import pytest

from application.factories import create_app
from application.database import db

import config

from utils import create_test_dummy_data


@pytest.fixture(scope='session')
def app(request):
    """
    flask test application
    :param request:
    :return:
    """
    # initialize flask application
    app = create_app('test_app', config.TestConfig)

    # initialize database
    with app.app_context():
        metadata = MetaData(db.engine)
        metadata.reflect()

        # drop database
        metadata.drop_all()

        # create tables based on the models
        db.create_all()

        # insert test data
        create_test_dummy_data()

        yield app

        # remove temporary tables in database
        # metadata.drop_all()


@pytest.fixture(scope='session')
def client(app):
    """
    test client for the app
    :param app:
    :return:
    """
    return app.test_client()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='ada@iws.com', password='lovelace'):
        return self._client.post(
            '/login',
            data={'email': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
