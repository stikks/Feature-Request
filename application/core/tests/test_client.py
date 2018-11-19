import pytest

from wtforms.validators import ValidationError

from sqlalchemy.exc import InvalidRequestError, DataError, DatabaseError

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


def test_create_client_empty_data(app):
    """
    tests creating client record with no
    data passed
    :param app:
    :return:
    """
    with pytest.raises(ValidationError):
        client.ClientService.objects_new()


def test_create_client_invalid_data_type(app):
    """
    tests creating client record with
    invalid arguments passed on name
    :param app:
    :return:
    """
    with pytest.raises(TypeError):
        client.ClientService.objects_new(**dict(
            name=1
        ))


def test_create_client_incomplete_data(app):
    """
    tests creating client record with
    incomplete data
    :param app:
    :return:
    """
    with pytest.raises(ValidationError):
        client.ClientService.objects_new(**dict(
            name=''
        ))


def test_get_client():
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


def test_get_client_invalid_id():
    """
    tests querying client records
    with non-existent id
    :param app:
    :return:
    """

    # retrieve new object from db
    # no client record exists with id - 100
    # should return None
    obj = client.ClientService.objects_get(100)

    # asserts if object is returned
    assert obj is None


def test_get_client_no_query_params():
    """
    tests querying client records
    with no query params
    :param app:
    :return:
    """
    with pytest.raises(TypeError):
        client.ClientService.objects_get()


def test_get_client_invalid_data_type(app):
    """
    tests querying client records
    with invalid query params
    :param app:
    :return:
    """
    with pytest.raises(DataError):
        client.ClientService.objects_get('a')


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


def test_filter_client_nonexistent_params():
    """
    test filtering clients on nonexistent paramters
    :return:
    """
    # retrieve object with inaccurate parameters
    obj = client.ClientService.objects_filter(**dict(slug='slugs'))

    # assert false, object not found
    assert obj is None


def test_filter_request_invalid_query_params():
    """
    tests invalid request error
    :return:
    """
    with pytest.raises(InvalidRequestError):
        client.ClientService.objects_filter(**dict(researcher='Lux Soap'))


def test_filter_client_no_query_params():
    """
    test client record filtering with
    no parameters passed
    returns one record
    :return:
    """

    # retrieve object with inaccurate parameters
    obj = client.ClientService.objects_filter()

    # assert response is type list
    assert isinstance(obj, models.Client)


def test_filter_account_no_query_params_first_only():
    """
    test client record filtering with
    no parameters passed
    returns multiple records
    :return:
    """

    # retrieve object with inaccurate parameters
    obj = client.ClientService.objects_filter(first_only=False)

    # assert response is type list
    assert isinstance(obj, list)

    # assert list not empty
    assert len(obj) >= 1


def test_all_clients():
    """
    test retrieve all clients
    :return:
    """
    # retrieve multiple objects
    client_list = client.ClientService.objects_all()

    # asserts true, length of list > 1
    assert len(client_list) > 1