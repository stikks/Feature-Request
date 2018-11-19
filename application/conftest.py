from sqlalchemy.schema import MetaData, DropConstraint
import pytest

from flask_wtf.csrf import generate_csrf
from flask_pytest import FlaskPytest

from application.factories import create_app
from application.database import db

import config

from utils import create_dummy_data


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
        create_dummy_data()

        app = FlaskPytest(app)

        yield app

        # remove temporary tables in database
        request.addfinalizer(metadata.drop_all)


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
            data={'email': username, 'password': password, 'csrf_token': generate_csrf()}
        )

    def invalid_login(self, username='abc@iws.com', password='lovelorn'):
        return self._client.post(
            '/login',
            data={'email': username, 'password': password, 'csrf_token': generate_csrf()}
        )

    def logout(self):
        return self._client.get('/logout')


@pytest.fixture(scope='session')
def user(app):
    return


@pytest.fixture(scope='session')
def auth(client, app):

    @app.login_manager.user_loader
    def load_user(employee_id):
        """
        returns user object if session authenticated
        else None
        :param employee_id:
        :return:
        """
        from application.core.services import account
        return account.EmployeeService.objects_get(employee_id)

    return AuthActions(client)
