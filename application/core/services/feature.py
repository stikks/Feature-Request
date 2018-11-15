"""
feature requests service layer
"""

from application.core import models

from application.core.services import BaseService

from application.database import db

BaseFeatureRequestService = BaseService.create_model_service(models.FeatureRequest)
ProductAreaService = BaseService.create_model_service(models.ProductArea)


class FeatureRequestService(BaseFeatureRequestService):
    """
    featureequest service class

    custom modification to base class
    basefeaturerequestservice to accomodate
    re-ordering of priorities
    """

    @classmethod
    def objects_new(cls, client_id, title, description, product_area_id, priority, target_date):
        """
        create new feature request object

        updates base class method
        :param client_id
        :param title
        :param description
        :param product_area_id
        :param priority
        :param target_date
        :return:
        """
        # re-order feature requests with a priority greater than/equal
        # to the new feature request, before creating the new
        # feature request if a feature request with such priority exists
        if cls.objects_filter(**dict(client_id=client_id, priority=priority)):
            cls.reorder_priorities(client_id=client_id, priority=priority)

        record = cls.model_class(
            title=title,
            description=description,
            client_id=client_id,
            product_area_id=product_area_id,
            priority=priority,
            target_date=target_date
        )
        db.session.add(record)
        db.session.commit()

        return record

    @staticmethod
    def reorder_priorities(client_id, priority):
        """
        re-order priorities on current feature requests
        :param client_id:
        :param priority
        :return:
        """
        model_class = BaseFeatureRequestService.model_class

        feature_request_query = model_class.query.filter(model_class.client_id == client_id,
                                                         model_class.priority >= priority).order_by(
                                                             model_class.priority.asc())
        if not feature_request_query.count():
            return True

        feature_requests = feature_request_query.all()

        for feature_request in feature_requests:

            # increment priority on each feature
            # request by 1
            feature_request.priority += 1
            db.session.add(feature_request)
            db.session.commit()

        return True
