"""
account service layer
"""
from flask import current_app
from flask_login import login_user, logout_user

from application import models

from . import BaseService


EmployeeService = BaseService.create_model_service(models.Employee)


def register(email, password, first_name, last_name):
    """

    creates new employee account

    creates a new employee account using provided input
    credentials. returns employee model object if new
    employee created else raise an exception

    :param email:
    :param password:
    :param first_name:
    :param last_name:
    :return:
    """

    try:
        return EmployeeService.objects_new(**dict(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=current_app.bcrypt.generate_password_hash(password).decode('utf-8')
        ))
    except Exception as error:
        raise error


def login(email, password, remember=False):
    """
    authenticates a employee using given email and password

    This authenticates a employee with the input email and
    password. if employee not found or credentials invalid,
    returns None else returns employee

    :param email:
    :param password:
    :param remember
    :return:
    """

    # check if employee exists
    employee = EmployeeService.objects_filter(**dict(email=email), first_only=True)

    # if user and passwords match, login user
    # and return user object
    if employee and current_app.bcrypt.check_password_hash(employee.password, password):
        login_user(employee, remember=remember)
        return employee

    return None


def logout():
    """
    Logs out a employee

    :param employee:
    :return:
    """

    return logout_user()
