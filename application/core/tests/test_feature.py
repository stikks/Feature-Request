from datetime import date, timedelta

import pytest

from sqlalchemy.exc import InvalidRequestError, DataError

from application.core.services import feature

from application.core import models


def test_create_feature_request():
    """
    tests creating a feature request
    :param app:
    :return:
    """
    obj = feature.FeatureRequestService.objects_new(
        client_id=1,
        title='Nivea',
        description='Design new page for nivea cream product',
        product_area_id=1,
        priority=1,
        target_date=date.today() + timedelta(days=20)
    )

    # asserts if object returned is an instance of
    # feature request model
    assert isinstance(obj, models.FeatureRequest)

    # asserts object priority
    assert obj.priority == 1


def test_reorder_priorities():
    """
    test reordering of priorities
    :return:
    """
    # insert first record
    obj = feature.FeatureRequestService.objects_new(
        client_id=1,
        title='Nivea Olive Oil',
        description='Design new landing page for nivea olive oil product',
        product_area_id=3,
        priority=2,
        target_date=date.today() + timedelta(days=22)
    )

    # insert second dummy feature request data
    feature.FeatureRequestService.objects_new(
        client_id=1,
        title='Nivea Oil',
        description='Design new page for nivea oil product',
        product_area_id=2,
        priority=2,
        target_date=date.today() + timedelta(days=30)
    )

    # asserts if priority of first feature request is changed.
    # retrieve new state from db
    obj = feature.FeatureRequestService.objects_get(obj.id)

    assert obj.priority == 3


def test_create_feature_request_no_data():
    """
    tests creating a feature request
    with no data passed
    :param app:
    :return:
    """
    with pytest.raises(TypeError):
        feature.FeatureRequestService.objects_new()


def test_create_feature_request_missing_field():
    """
    tests creating a feature request
    with one or more missing fields
    :param app:
    :return:
    """
    # with one missing field
    with pytest.raises(TypeError):
        feature.FeatureRequestService.objects_new(
            client_id=1,
            title='One Piece',
            description='Chart a course for All Blue',
            product_area_id=2,
            priority=2
        )

    # with 2 missing fields
    with pytest.raises(TypeError):
        feature.FeatureRequestService.objects_new(
            client_id=1,
            title='One Piece',
            description='Chart a course for All Blue',
            product_area_id=2
        )


def test_create_feature_request_invalid_data_type():
    """
    tests create a feature request with an invalida data type
    on priority
    :return:
    """
    with pytest.raises(DataError):
        feature.FeatureRequestService.objects_new(
            client_id=1,
            title='Nivea Oil',
            description='Design new page for nivea oil product',
            product_area_id=2,
            priority='lords',
            target_date=date.today() + timedelta(days=30)
        )


def test_create_feature_request_invalid_foreign_key():
    """
    tests create with an invalid foreign key
    :return:
    """
    # testing with invalid client id
    with pytest.raises(ValueError):
        feature.FeatureRequestService.objects_new(
            client_id=250,
            title='Nivea Oil',
            description='Design new page for nivea oil product',
            product_area_id=2,
            priority=1,
            target_date=date.today() + timedelta(days=30)
        )

    # testing with invalid product area id
    with pytest.raises(ValueError):
        feature.FeatureRequestService.objects_new(
            client_id=1,
            title='Nivea Oil',
            description='Design new page for nivea oil product',
            product_area_id=25,
            priority=1,
            target_date=date.today() + timedelta(days=30)
        )


def test_get_feature_request(app):
    """
    tests retrieving a feature request
    :param app:
    :return:
    """
    # retrieve object from db
    obj = feature.FeatureRequestService.objects_get(1)

    # asserts if object is returned
    assert obj.id is not None

    # asserts if object returned is an instance of
    # feature request model
    assert isinstance(obj, models.FeatureRequest)

    # asserts true if id of object is 1
    assert obj.id == 1


def test_get_feature_request_non_existent_data():
    """
    tests feature request get with non existent data
    :return:
    """
    # retrieve new object from db
    obj = feature.FeatureRequestService.objects_get(20)

    # asserts if object is returned
    assert obj is None


def test_get_feature_request_no_query_params():
    """
    tests querying feature request records
    with no query params
    :return:
    """
    with pytest.raises(TypeError):
        feature.FeatureRequestService.objects_get()


def test_get_feature_request_invalid_data_type(app):
    """
    tests querying feature request records
    with no query params
    :param app:
    :return:
    """
    with pytest.raises(DataError):
        feature.FeatureRequestService.objects_get('a')


def test_filter_feature_request_single():
    """
    test feature request
    :return:
    """
    # retrieve object from db
    # based on feature request created
    # above, returning only one object
    obj = feature.FeatureRequestService.objects_filter(**dict(client_id=1, title='Nivea Oil'))

    # asserts if object is returned
    assert obj.id is not None

    # asserts if object returned is an instance of
    # feature request model
    assert isinstance(obj, models.FeatureRequest)

    # asserts object returned is accurate
    # test client_id and title
    assert obj.client_id == 1
    assert obj.title == 'Nivea Oil'


def test_filter_feature_request_list():
    """
    tests filter feature request service
    returns list
    :return:
    """
    # retrieve multiple objects
    feature_list = feature.FeatureRequestService.objects_filter(first_only=False, **dict(client_id=1))

    # asserts true, length of list >= 1
    assert len(feature_list) >= 1


def test_filter_feature_request_nonexistent_data_single():
    """
    tests filter feature request with non existent data
    :return:
    """
    # retrieve object with non existent data
    obj = feature.FeatureRequestService.objects_filter(**dict(client_id=1, title='Nivea Oils'))

    # assert false, object not found
    assert obj is None


def test_filter_feature_request_nonexistent_data_list():
    """
    tests filter feature request with non existent data
    :return:
    """
    # retrieve object with inaccurate parameters
    obj_list = feature.FeatureRequestService.objects_filter(first_only=False, **dict(client_id=190))

    # assert false, object not found
    assert len(obj_list) == 0


def test_filter_request_invalid_parameter():
    """
    tests invalid request error
    :return:
    """
    with pytest.raises(InvalidRequestError):
        feature.FeatureRequestService.objects_filter(**dict(client_slug='marvel-studios'))


def test_all_feature_requests():
    """
    test retrieve all feature requests
    :return:
    """
    # retrieve multiple objects
    feature_list = feature.FeatureRequestService.objects_all()

    # asserts true, length of list > 1
    assert len(feature_list) >= 1


def test_create_product_area():
    """
    tests creating a product area
    :return:
    """
    obj = feature.ProductAreaService.objects_new(
        title='Charity Work'
    )

    # asserts if object returned is an instance of
    # product area model
    assert isinstance(obj, models.ProductArea)

    # asserts object slug
    assert obj.slug == 'charity-work'


def test_get_product_area():
    """
    tests retrieving a product area
    :return:
    """
    # retrieve object from db
    obj = feature.ProductAreaService.objects_get(1)

    # asserts if object is returned
    assert obj.id is not None

    # asserts if object returned is an instance of
    # product area model
    assert isinstance(obj, models.ProductArea)

    # asserts true if id of object is 1
    assert obj.id == 1


def test_get_product_area_nonexistent_data():
    """
    tests get product area non-existent data
    :return:
    """
    # retrieve new object from db
    obj = feature.ProductAreaService.objects_get(220)

    # asserts if object is returned
    assert obj is None


def test_filter_product_area_single():
    """
    test product area filtering
    :return:
    """
    # retrieve object from db
    # based on feature request created
    # above, returning only one object
    obj = feature.ProductAreaService.objects_filter(**dict(slug='charity-work'))

    # asserts if object is returned
    assert obj.id is not None

    # asserts if object returned is an instance of
    # product area model
    assert isinstance(obj, models.ProductArea)

    # asserts object returned is accurate
    # test slug and title
    assert obj.slug == 'charity-work'
    assert obj.title == 'Charity Work'


def test_filter_product_area_list():
    """
    tests product area filter service list
    :return:
    """
    obj_list = feature.ProductAreaService.objects_filter(first_only=False, **dict(slug='reports'))

    assert len(obj_list) == 1


def test_filter_product_area_nonexistent_data_single():
    """
    tests filter product area service with
    non existent data
    :return:
    """
    # retrieve object with inaccurate parameters
    obj = feature.ProductAreaService.objects_filter(**dict(slug='ninja-assasin'))

    # assert false, object not found
    assert obj is None


def test_filter_product_area_nonexistent_data_list():
    """
    tests filter product area service with
    non existent data
    returns list
    :return:
    """
    # retrieve object with inaccurate parameters
    obj_list = feature.ProductAreaService.objects_filter(first_only=False, **dict(slug='ninja-assasin'))

    # assert false, object not found
    assert len(obj_list) == 0


def test_filter_product_area_no_params_single():
    """
    tests filter product area no parameter passed
    single object query
    :return:
    """
    # retrieve multiple objects
    product_area = feature.ProductAreaService.objects_filter(**dict())

    # asserts None
    assert isinstance(product_area, models.ProductArea)


def test_filter_product_area_no_params_list():
    """
    tests filter product area no parameter passed
    list query
    :return:
    """
    # retrieve multiple objects
    product_list = feature.ProductAreaService.objects_filter(first_only=False, **dict())

    # asserts true, length of list >= 1
    assert len(product_list) >= 1


def test_filter_product_area_invalid_paramters():
    """
    tests invalid request error on product
    area query
    :return:
    """
    with pytest.raises(InvalidRequestError):
        feature.ProductAreaService.objects_filter(**dict(area='cleaning'))


def test_all_product_areas():
    """
    test retrieve all product areas
    :return:
    """
    # retrieve multiple objects
    product_list = feature.ProductAreaService.objects_all()

    # asserts true, length of list > 1
    assert len(product_list) > 1
