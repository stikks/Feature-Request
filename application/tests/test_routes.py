def test_login_view(client):
    """
    tests login view
    :param client:
    :return:
    """
    # test that viewing the page renders without template errors
    assert client.get('/login').status_code == 200


def test_login_redirect(client, auth):
    """
    tests login redirect on protected pages
    :return:
    """
    with client:
        # logs out any current sessions
        auth.logout()

        # checks 302 url found redirection
        assert client.get('/').status_code == 302


def test_homepage_view(client, auth):
    """
    tests home page request after logging in
    :param client:
    :param auth:
    :return:
    """
    with client:

        # logs in user with valid credentials
        auth.login()

        # test that viewing the page renders without template errors
        assert client.get('/').status_code == 200


def test_client_view(client, auth):
    """
    tests clients list page request after logging in
    :param client:
    :param auth:
    :return:
    """
    with client:

        # logs in user with valid credentials
        auth.login()

        # test that viewing the page renders without template errors
        assert client.get('/clients').status_code == 200


def test_client_a_feature_request_view(client, auth):
    """
    tests client a feature request list page
    request after logging in
    :param client:
    :param auth:
    :return:
    """
    with client:

        # logs in user with valid credentials
        auth.login()

        # test that viewing the page renders without template errors
        assert client.get('/clients/client-a/feature-requests').status_code == 200


def test_client_a_feature_request_create_view(client, auth):
    """
    tests client a create new feature request page
    request after logging in
    :param client:
    :param auth:
    :return:
    """
    with client:

        # logs in user with valid credentials
        auth.login()

        # test that viewing the page renders without template errors
        assert client.get('/clients/client-a/feature-requests/new').status_code == 200


def test_invalid_client_feature_request_view(client, auth):
    """
    tests invalid list feature request page
    request after logging in
    :param client:
    :param auth:
    :return:
    """
    with client:

        # logs in user with valid credentials
        auth.login()

        # test that viewing the page renders without template errors
        assert client.get('/clients/client-invalid/feature-requests').status_code == 404


def test_invalid_client_feature_request_create_view(client, auth):
    """
    tests invalid create new feature request page
    request after logging in
    :param client:
    :param auth:
    :return:
    """
    with client:

        # logs in user with valid credentials
        auth.login()

        # test that viewing the page renders without template errors
        assert client.get('/clients/client-invalid/feature-requests/new').status_code == 404

