"""
application schemas
"""
from flask import current_app
from marshmallow import fields

from . import models


class ClientSchema(current_app.marshmallow.ModelSchema):
    """
    Client model schema
    """
    class Meta:
        """ meta attributes of client model schema """
        model = models.Client


class ProductAreaSchema(current_app.marshmallow.ModelSchema):
    """ProductArea model schema"""
    class Meta:
        """ meta attributes of productarea model schema  """
        model = models.ProductArea


class FeatureRequestSchema(current_app.marshmallow.ModelSchema):
    """FeatureRequest model schema"""
    class Meta:
        """ meta attributes of featurerequest model schema """
        model = models.FeatureRequest
        fields = ('id', 'title', 'description', 'client', 'product_area', 'priority', 'target_date', 'date_created',
                  'date_updated')
    client = fields.Nested(ClientSchema)
    product_area = fields.Nested(ProductAreaSchema)