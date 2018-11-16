"""
test database connection
"""

from application.database import db

from application.core import models


def test_db(client):
    """
    test db connection
    :param client:
    :return:
    """
    # test if dummy employee object inserted into db
    assert db.session.query(models.Employee).count() >= 1
