"""
client service layer
"""

from application.core import models

from application.core.services import BaseService

from application import forms


ClientService = BaseService.create_model_service(models.Client, forms.ClientForm)
