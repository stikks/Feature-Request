import pytest

from sqlalchemy.exc import InvalidRequestError

from application.core.services import client

from application.core import models


def test_create_client(app):
    """
    tests creating a client
    :param app:
    :return:
    """
    client_obj = client.ClientService.objects_new(**dict(
        name='Marvel Studios'
    ))

    # asserts if object returned is an instance of
    # client model
    assert isinstance(client_obj, models.Client)

    # asserts if object parameters are correct
    assert client_obj.slug == 'marvel-studios'


def test_get_client(app):
    """
    tests retrieving a feature request
    :param app:
    :return:
    """
    # retrieve object from db
    obj = client.ClientService.objects_get(1)

    # asserts if object is returned
    assert obj.id is not None

    # asserts if object returned is an instance of
    # client model
    assert isinstance(obj, models.Client)

    # asserts true if id of object is 1
    assert obj.id == 1

    # retrieve new object from db
    obj = client.ClientService.objects_get(100)

    # asserts if object is returned
    assert obj is None


def test_filter_client():
    """
    test filtering client
    :return:
    """
    # retrieve object from db
    # based on client object created
    # above, returning only one object
    obj = client.ClientService.objects_filter(**dict(slug='marvel-studios'))

    # asserts if object is returned
    assert obj.id is not None

    # asserts if object returned is an instance of
    # feature request model
    assert isinstance(obj, models.Client)

    # asserts object returned is accurate
    # test slug and name
    assert obj.slug == 'marvel-studios'
    assert obj.name == 'Marvel Studios'

    # retrieve object with inaccurate parameters
    obj = client.ClientService.objects_filter(**dict(slug='slugs'))

    # assert false, object not found
    assert obj is None


def test_invalid_request_error():
    """
    tests invalid request error
    :return:
    """
    with pytest.raises(InvalidRequestError):
        client.ClientService.objects_filter(**dict(researcher='Lux Soap'))


def test_all_clients():
    """
    test retrieve all clients
    :return:
    """
    # retrieve multiple objects
    client_list = client.ClientService.objects_all()

    # asserts true, length of list > 1
    assert len(client_list) > 1