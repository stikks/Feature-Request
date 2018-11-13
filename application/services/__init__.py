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
            def objects_all(cls):
                """
                retrieve all model objects
                :return:
                """
                return cls.model_class.query.all()

            @classmethod
            def objects_filter(cls, first_only=True, **kwargs):
                """
                retrieve objects matching filter params

                returns a filtered query result for a model.
                If first_only passed as True, first object is
                returned else list of objects returned.
                :param first_only
                :param kwargs:
                :return:
                """
                try:
                    filtered = cls.model_class.query.filter_by(**kwargs)
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
