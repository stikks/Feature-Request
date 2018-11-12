from application import models


def feature_requests_all():
    """
    returns list of registered clients
    :return:
    """
    return models.Client.query.all()


def feature_requests_new(first_name, last_name, email):
    """
    creates a new client

    creates new entry in clients table using provided
    parameters. It returns a new client object if created
    else it raises an exception

    :param first_name:
    :param last_name:
    :param email:
    :return:
    """

    try:
        return models.Client.create(first_name=first_name, last_name=last_name, email=email)
    except Exception:
        raise
