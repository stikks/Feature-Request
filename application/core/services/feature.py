"""
feature requests service layer
"""

from application.core import models

from application.core.services import BaseService, client as client_service

from application.database import db

from application import forms


BaseFeatureRequestService = BaseService.create_model_service(models.FeatureRequest, forms.FeatureRequestForm)
ProductAreaService = BaseService.create_model_service(models.ProductArea, forms.ProductAreaForm)


class FeatureRequestService(BaseFeatureRequestService):
    """
    feature equest service class

    custom modification to base class
    basefeaturerequest service to accommodate
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
        # verify client
        client = client_service.ClientService.objects_get(client_id)

        if not client:
            raise ValueError('Client with id - {} not found'.format(client_id))

        # verify product area
        product_area = ProductAreaService.objects_get(product_area_id)

        if not product_area:
            raise ValueError('ProductArea with id - {} not found'.format(product_area_id))

        # re-order feature requests with a priority greater than/equal
        # to the new feature request, before creating the new
        # feature request if a feature request with such priority exists
        if cls.objects_filter(**dict(client_id=client.id, priority=priority)):
            cls.reorder_priorities(client_id=client.id, priority=priority)

        record = BaseFeatureRequestService.objects_new(
            title=title,
            description=description,
            client_id=client.id,
            product_area_id=product_area.id,
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

    @staticmethod
    def compute_max_value():
        """
        computes max value of currently stored feature requests
        :return:
        """
        model_class = BaseFeatureRequestService.model_class

        sub = db.session.query(db.func.max(model_class.priority).label('ml')).subquery()
        feature_request = db.session.query(model_class).join(sub, sub.c.ml == model_class.priority).first()
        return feature_request.priority + 1 if feature_request else 1
