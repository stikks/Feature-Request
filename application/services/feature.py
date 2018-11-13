from application import models

from application.services import BaseService


FeatureService = BaseService.create_model_service(models.FeatureRequest)
ProductAreaService = BaseService.create_model_service(models.ProductArea)
