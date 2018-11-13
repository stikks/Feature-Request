from application import models

from application.services import BaseService


ClientService = BaseService.create_model_service(models.Client)
