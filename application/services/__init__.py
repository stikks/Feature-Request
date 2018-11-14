# for class check
import inspect
from sqlalchemy.exc import InvalidRequestError, DataError

from application.models import db, current_app

logger = getattr(current_app, 'logger')


class BaseService(object):

    @classmethod
    def create_model_service(cls, model_class):
        """
        creates a class with CRUD methods

        creates a class that has create, retrieve,
        update and delete methods for a specific model

        :param model_class:
        :return:
        """
        class Base(object):

            @classmethod
            def objects_all(cls, order_by='date_created', order_direction='desc',):
                """
                retrieve all model objects

                orders model list by date_created if no value passed
                :param order_by
                :param order_direction 
                :return:
                """
                order_field = getattr(cls.model_class, order_by)
                order_method = getattr(order_field, order_direction)
                return cls.model_class.query.order_by(order_method()).all()

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
                :param kwargs:
                :return:
                """
                try:
                    order_field = getattr(cls.model_class, order_by)
                    order_method = getattr(order_field, order_direction)
                    filtered = cls.model_class.query.filter_by(**kwargs).order_by(order_method())
                    return filtered.first() if first_only else filtered.all()
                except InvalidRequestError as e:
                    logger.exception(e)
                    raise e
                except Exception as e:
                    logger.exception(e)
                    raise e

            @classmethod
            def objects_get(cls, pk):
                """

                :param pk:
                :return:
                """
                try:
                    return cls.model_class.query.get(pk)
                except DataError as e:
                    logger.exception(e)
                    raise
                except Exception as e:
                    logger.exception(e)
                    raise e

            @classmethod
            def objects_new(cls, **kwargs):
                """
                create new model object
                :param kwargs:
                :return:
                """
                record = cls.model_class(**kwargs)
                db.session.add(record)
                db.session.commit()
                return record

        # raise error if model_class input not a class
        if not inspect.isclass(model_class):
            raise TypeError("Invalid data type, needs to be a subclass of 'sqlalchemy.ext.declarative.api.Model'")

        if not issubclass(model_class, db.Model):
            raise TypeError("Invalid model class, should be a subclass of 'sqlalchemy.ext.declarative.api.Model'")

        Base.model_class = model_class
        return Base
