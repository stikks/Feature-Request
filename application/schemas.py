from flask import current_app

from . import models


class ClientSchema(current_app.marshmallow.ModelSchema):
    class Meta:
        model = models.Client


class FeatureRequestSchema(current_app.marshmallow.ModelSchema):
    class Meta:
        model = models.FeatureRequest
