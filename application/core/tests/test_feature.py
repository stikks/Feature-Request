from datetime import date, timedelta

import pytest

from sqlalchemy.exc import InvalidRequestError

from application.core.services import feature

from application.core import models


def test_create_feature_request(app):
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

    # insert second dummy feature request data
    feature.FeatureRequestService.objects_new(
        client_id=1,
        title='Nivea Oil',
        description='Design new page for nivea oil product',
        product_area_id=2,
        priority=1,
        target_date=date.today() + timedelta(days=30)
    )

    # asserts if priority of first feature request changed
    # retrieve new state from db
    obj = feature.FeatureRequestService.objects_get(obj.id)

    assert obj.priority == 2


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

    # retrieve new object from db
    obj = feature.FeatureRequestService.objects_get(20)

    # asserts if object is returned
    assert obj is None


def test_filter_feature_request():
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

    # retrieve object with inaccurate parameters
    obj = feature.FeatureRequestService.objects_filter(**dict(client_id=1, title='Nivea Oils'))

    # assert false, object not found
    assert obj is None

    # retrieve multiple objects
    feature_list = feature.FeatureRequestService.objects_filter(first_only=False, **dict(client_id=1))

    # asserts true, length of list >= 1
    assert len(feature_list) >= 1


def test_invalid_request_error():
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
    assert len(feature_list) > 1


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

    # retrieve new object from db
    obj = feature.ProductAreaService.objects_get(220)

    # asserts if object is returned
    assert obj is None


def test_filter_product_area():
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

    # retrieve object with inaccurate parameters
    obj = feature.ProductAreaService.objects_filter(**dict(slug='ninja-assasin'))

    # assert false, object not found
    assert obj is None

    # retrieve multiple objects
    product_list = feature.ProductAreaService.objects_filter(first_only=False, **dict())

    # asserts true, length of list >= 1
    assert len(product_list) >= 1


def test_product_area_invalid_request_error():
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
