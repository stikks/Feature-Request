"""
service initialization module
"""
# for class check
import inspect
from sqlalchemy.exc import InvalidRequestError, DataError, IntegrityError

from flask import current_app
from wtforms.validators import ValidationError

from application.database import db

logger = getattr(current_app, 'logger')


class BaseService(object):
    """
    Factory service for creating creating classes
    with CRUD methods, related to model
    """

    @classmethod
    def create_model_service(cls, model_class, form_class):
        """
        creates a class with CRUD methods

        creates a class that has create, retrieve,
        update and delete methods for a specific model

        :param model_class:
        :param form_class
        :return:
        """
        class Base(object):
            """
            class with CRUD methods, 
            associated with specific model
            """

            @staticmethod
            def rollback_and_log(error):
                db.session.rollback()
                logger.exception(error)

            @classmethod
            def objects_all(cls, order_by='date_created', order_direction='desc',):
                """
                retrieve all model objects

                orders model list by date_created if no value passed
                :param order_by
                :param order_direction
                :return:
                """
                order_field = getattr(model_class, order_by)
                order_method = getattr(order_field, order_direction)
                return db.session.query(model_class).order_by(order_method()).all()

            @classmethod
            def objects_filter(cls, first_only=True, order_by='date_created', order_direction='desc', **kwargs):
                """
                retrieve objects matching filter params

                returns a filtered query result for a model.
                If first_only passed as True, first object is
                returned else list of objects returned.
                orders list by date_created in descending order 
                if order_by and order_direction not passed.

                :param first_only
                :param order_by
                :param order_direction
                :param kwargs:
                :return:
                """
                try:
                    order_field = getattr(model_class, order_by)
                    order_method = getattr(order_field, order_direction)

                    filtered = db.session.query(model_class).filter_by(**kwargs).order_by(order_method())

                    return filtered.first() if first_only else filtered.all()
                except InvalidRequestError as error:
                    cls.rollback_and_log(error)
                    raise error

                except Exception as error:
                    cls.rollback_and_log(error)
                    raise error

            @classmethod
            def objects_get(cls, obj_id):
                """
                retrieves object with matching obj_id
                :param obj_id:
                :return:
                """
                try:
                    return db.session.query(model_class).get(obj_id)
                except DataError as error:
                    cls.rollback_and_log(error)
                    raise

                except InvalidRequestError as error:
                    cls.rollback_and_log(error)
                    raise error

                except Exception as error:
                    cls.rollback_and_log(error)
                    raise error

            @classmethod
            def objects_new(cls, **kwargs):
                """
                create new model object
                :param kwargs:
                :return:
                """

                form = form_class(**kwargs)

                if not form.validate():
                    raise ValidationError(form.errors)

                try:
                    record = model_class(**form.data)
                    db.session.add(record)
                    db.session.commit()
                    return record
                except IntegrityError as error:
                    cls.rollback_and_log(error)
                    raise error
                except Exception as error:
                    cls.rollback_and_log(error)
                    raise error

        # raise error if model_class input not a class
        if not inspect.isclass(model_class):
            raise TypeError("Invalid data type, needs to be a subclass of 'sqlalchemy.ext.declarative.api.Model'")

        if not issubclass(model_class, db.Model):
            raise TypeError("Invalid model class, should be a subclass of 'sqlalchemy.ext.declarative.api.Model'")

        Base.model_class = model_class
        Base.form_class = form_class
        return Base
