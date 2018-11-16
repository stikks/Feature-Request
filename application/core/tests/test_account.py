import pytest

from sqlalchemy.exc import InvalidRequestError

from application.core.services import account

from application.core import models


def test_create_employee(client, app):
    """
    tests creating an employee
    :param client:
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


def test_get_account(app):
    """
    tests retrieving n employee account
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

    # retrieve new object from db
    obj = account.EmployeeService.objects_get(10)

    # asserts if object is returned
    assert obj is None


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

    # retrieve object with inaccurate parameters
    obj = account.EmployeeService.objects_filter(**dict(first_name='Barney'))

    # assert false, object not found
    assert obj is None


def test_invalid_request_error():
    """
    tests invalid request error
    :return:
    """
    with pytest.raises(InvalidRequestError):
        account.EmployeeService.objects_filter(**dict(name='Stinson'))


def test_all_accounts():
    """
    test retrieve all employee accounts
    :return:
    """
    # retrieve multiple objects
    employee_list = account.EmployeeService.objects_all()

    # asserts true, length of list > 1
    assert len(employee_list) > 1


