import pytest

from sqlalchemy.exc import InvalidRequestError, IntegrityError, DataError

import psycopg2
from wtforms.validators import ValidationError

from application.core.services import account

from application.core import models


def test_create_employee(app):
    """
    tests creating an employee
    :param app:
    :return:
    """
    employee = account.EmployeeService.objects_new(**dict(
        first_name='Frederik',
        last_name='Douglas',
        email='frederik@iws.com',
        password=app.bcrypt.generate_password_hash('frederik').decode('utf-8')
    ))

    # asserts true if employee is an instance of
    # employee model
    assert isinstance(employee, models.Employee)

    # asserts true if object parameter correct
    assert employee.email == 'frederik@iws.com'

    # asserts false for valid password confirmation
    # wrong password used for test
    assert app.bcrypt.check_password_hash(employee.password, 'frederick') is False

    # asserts true for valid password check
    assert app.bcrypt.check_password_hash(employee.password, 'frederik') is True


def test_create_employee_empty_data(app):
    """
    tests creating employee record with no
    data passed
    :param app:
    :return:
    """
    with pytest.raises(ValidationError):
        account.EmployeeService.objects_new()


def test_create_employee_invalid_data_type(app):
    """
    tests creating employee record with
    invalid arguments passed on email
    :param app:
    :return:
    """
    with pytest.raises(TypeError):
        account.EmployeeService.objects_new(**dict(
            first_name='Frederik',
            last_name='Douglas',
            email=1,
            password=app.bcrypt.generate_password_hash('frederik').decode('utf-8')
        ))


def test_create_employee_incomplete_data(app):
    """
    tests creating employee record with
    incomplete data
    :param app:
    :return:
    """
    with pytest.raises(ValidationError):
        account.EmployeeService.objects_new(**dict(
            first_name='Marie',
            last_name='Curie',
            email='',
            password=app.bcrypt.generate_password_hash('frederik').decode('utf-8')
        ))


def test_create_employee_unique_email(app):
    """
    tests creating employee record with
    incomplete data
    :param app:
    :return:
    """
    with pytest.raises(IntegrityError):
        account.EmployeeService.objects_new(**dict(
            first_name='Frankie',
            last_name='De Licht',
            email='ada@iws.com',
            password=app.bcrypt.generate_password_hash('frederik').decode('utf-8')
        ))


def test_get_account():
    """
    tests retrieving an employee account
    :param app:
    :return:
    """
    # retrieve object from db
    obj = account.EmployeeService.objects_get(1)

    # asserts if object is returned
    assert obj.id is not None

    # asserts if object returned is an instance of
    # employee model
    assert isinstance(obj, models.Employee)

    # asserts true if id of object is 1
    assert obj.id == 1


def test_get_account_invalid_id():
    """
    tests querying employee records
    with non-existent id
    :param app:
    :return:
    """

    # retrieve new object from db
    # no employee record exists with id - 10
    # should return None
    obj = account.EmployeeService.objects_get(10)

    # asserts if object is returned
    assert obj is None


def test_get_account_no_query_params():
    """
    tests querying employee records
    with no query params
    :param app:
    :return:
    """
    with pytest.raises(TypeError):
        account.EmployeeService.objects_get()


def test_get_account_invalid_data_type(app):
    """
    tests querying employee records
    with no query params
    :param app:
    :return:
    """
    with pytest.raises(DataError):
        account.EmployeeService.objects_get('a')


def test_filter_account():
    """
    test filtering account
    :return:
    """
    # retrieve object from db
    # based on client object created
    # above, returning only one object
    obj = account.EmployeeService.objects_filter(**dict(email='frederik@iws.com'))

    # asserts if object is returned
    assert obj.id is not None

    # asserts if object returned is an instance of
    # employee model
    assert isinstance(obj, models.Employee)

    # asserts object returned is accurate
    # test first_name, last_name and email
    assert obj.first_name == 'Frederik'
    assert obj.last_name == 'Douglas'
    assert obj.email == 'frederik@iws.com'


def test_filter_account_non_existing_data():
    """
    test employee record filtering with
    non existent data
    :return:
    """

    # retrieve object with inaccurate parameters
    obj = account.EmployeeService.objects_filter(**dict(first_name='Barney'))

    # assert false, object not found
    assert obj is None


def test_filter_account_no_query_params():
    """
    test employee record filtering with
    no parameters passed
    :return:
    """

    # retrieve object with inaccurate parameters
    obj = account.EmployeeService.objects_filter()

    # assert response is type list
    assert isinstance(obj, models.Employee)


def test_filter_account_no_query_params_first_only():
    """
    test employee record filtering with
    no parameters passed
    :return:
    """

    # retrieve object with inaccurate parameters
    obj = account.EmployeeService.objects_filter(first_only=False)

    # assert response is type list
    assert isinstance(obj, list)

    # assert list not empty
    assert len(obj) >= 1


def test_filter_account_invalid_query_param():
    """
    tests invalid request error
    :return:
    """
    # invalid key 'name'
    with pytest.raises(InvalidRequestError):
        account.EmployeeService.objects_filter(**dict(name='Stinson'))

    # invalid key 'emails'
    with pytest.raises(InvalidRequestError):
        account.EmployeeService.objects_filter(**dict(emails='frederik@iws.com'))


def test_all_accounts():
    """
    test retrieve all employee accounts
    :return:
    """
    # retrieve multiple objects
    employee_list = account.EmployeeService.objects_all()

    # asserts true, length of list > 1
    assert len(employee_list) > 1


