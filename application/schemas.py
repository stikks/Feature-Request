from flask import current_app
from marshmallow import fields

from . import models


class ClientSchema(current_app.marshmallow.ModelSchema):
    class Meta:
        model = models.Client


class ProductAreaSchema(current_app.marshmallow.ModelSchema):
    class Meta:
        model = models.ProductArea


class FeatureRequestSchema(current_app.marshmallow.ModelSchema):
    class Meta:
        model = models.FeatureRequest
        fields = ('id', 'title', 'description', 'client', 'product_area', 'client_priority', 'target_date', 'date_created', 'date_updated')
    # client = ClientSchema('client_id')
    client = fields.Nested(ClientSchema)
    product_area = fields.Nested(ProductAreaSchema)