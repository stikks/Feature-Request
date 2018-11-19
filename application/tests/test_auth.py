"""
test authentication
"""
from flask import session
from flask_login import current_user


def test_login_user(client, auth):
    """
    tests user login request
    :param client:
    :param auth:
    :return:
    """
    # test that successful login redirects to the index page
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/clients'

    # login request set the user_id in the session
    # check that the user is loaded from the session
    with client:
        client.get('/')

        # check against session
        assert session['user_id'] == '1'

        # check against flask login authentication check
        assert current_user.is_authenticated is True


def test_invalid_login_parameters(client, auth):
    """
    tests invalid login parameters
    :param client:
    :param auth:
    :return:
    """
    # test that successful login redirects to the index page
    with client:
        # logs out any current sessions
        auth.logout()

        # logs in using invalid parameters
        auth.invalid_login()

        # checks session
        assert session.get('user_id') is None

        # checks flask login authentication
        assert current_user.is_authenticated is False


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
