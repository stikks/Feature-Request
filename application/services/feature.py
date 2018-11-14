from application import models

from application.services import BaseService


BaseFeatureRequestService = BaseService.create_model_service(models.FeatureRequest)
ProductAreaService = BaseService.create_model_service(models.ProductArea)


class FeatureRequestService(BaseFeatureRequestService):

    @classmethod
    def objects_new(cls, client_id, title, description, product_area_id, **kwargs):
        """
        create new model object
        :param kwargs:
        :return:
        """
        # re-order participants
        cls.reorder_priorities()

        record = cls.model_class(**kwargs)
        models.db.session.add(record)
        models.db.session.commit()

        # reorder priorities

        return record

    @staticmethod
    def reorder_priorities(client_id):
        """
        """
        pass