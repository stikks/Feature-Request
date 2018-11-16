"""
test flask application
"""


def test_app(client):
    """
    test app
    :param client:
    :return:
    """
    # tests viewing page renders without template errors
    # and returns 200 with redirect set
    assert client.get('/', follow_redirects=True).status_code == 200

    # tests viewing page renders without template errors
    # and returns 302 without redirect set
    assert client.get('/').status_code == 302
