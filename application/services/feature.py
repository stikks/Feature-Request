from application import models

from application.services import BaseService

BaseFeatureRequestService = BaseService.create_model_service(models.FeatureRequest)
ProductAreaService = BaseService.create_model_service(models.ProductArea)


class FeatureRequestService(BaseFeatureRequestService):

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
        models.db.session.add(record)
        models.db.session.commit()

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

        feature_request = next((i for i in feature_requests if i.priority == priority), None)

        if not feature_request:
            return True

        feature_request.priority += 1
        models.db.session.add(feature_request)
        models.db.session.commit()

        filtered_requests = list(filter(lambda x: x.priority != priority, feature_requests))

        if len(filtered_requests) == 0:
            return True

        # feature_request = BaseFeatureRequestService.objects_filter(**dict(client_id=client_id, priority=priority))
        #
        # if not feature_request:
        #     return True
        i = 0
        current = feature_request
        while i < len(filtered_requests):
            # feature_request = BaseFeatureRequestService.objects_filter(**dict(client_id=client_id, priority=priority))
            #
            # if not feature_request:
            #     break

            current_feature_request = filtered_requests[i]

            if current_feature_request.priority - current.priority > 1:
                break

            current_feature_request.priority += 1
            models.db.session.add(current_feature_request)
            models.db.session.commit()

            current = current_feature_request

        # # retrieve feature requests with a priority greater than/equal to the new feature request
        # feature_request_query = model_class.query.filter(model_class.client_id == client_id,
        #                                                  model_class.priority >= priority).order_by(
        #                                                     model_class.priority.asc())
        # if not feature_request_query.count():
        #     return True
        #
        # feature_request_query_all = feature_request_query.all()
        #
        # priority_check = 0
        # while priority_check < len(feature_request_query_all):
        #
        #     # check if there's a feature request that matches current
        #     # iteration index
        #     current_feature_request = next((i for i in feature_request_query if i.priority == priority), None)
        #     if not current_feature_request:
        #         break
        #
        #     # increment priority of current feature request
        #     current_feature_request.priority += 1
        #     models.db.session.add(current_feature_request)
        #
        #     # save changes
        #     models.db.session.commit()
        #
        #     # increment and check for matching feature request
        #     priority_check += 1

        return True
