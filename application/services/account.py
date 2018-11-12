from flask_login import login_user, logout_user

from application import models


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
        return models.Employee.create(email=email, first_name=first_name, last_name=last_name)
    except Exception:
        raise


def login(email, password):
    """
    authenticates a user using given email and password

    This authenticates a user with the input email and
    password. if user not found or credentials invalid,
    returns None else returns user

    :param email:
    :param password:
    :return:
    """

    pass


def logout():
    """
    Logs out a user

    :param user:
    :return:
    """

    return logout_user()
