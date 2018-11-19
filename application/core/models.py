"""
application models
"""
import datetime

# import usermixin
from flask_login import UserMixin

# Import SQLAlchemy
from sqlalchemy.inspection import inspect
from sqlalchemy import event
from sqlalchemy_utils.types import EmailType

# import slugify
from slugify import slugify

from application.database import db


def generate_slug(target, value, oldvalue, initiator):
    """
    generates slug

    :param target
    :param value
    :param oldvalue
    :param initiator
    """
    if value and (not target.slug or value != oldvalue):
        target.slug = slugify(value)


class Serializer(object):
    """
    adds serialization to model objects
    """

    def serialize(self):
        """
        serialize model object
        :return:
        """
        output = dict()
        for key in inspect(self).attrs.keys():
            if key not in getattr(self, '__exclude__'):
                # retrieve attribute not excluded
                if isinstance(getattr(self, key), datetime.time):
                    output[key] = getattr(self, key).isoformat()
                elif isinstance(getattr(self, key), db.Model):
                    output[key] = getattr(self, key).serialize()
                else:
                    output[key] = getattr(self, key)

        return output

    @staticmethod
    def serialize_list(model_list):
        """
        returns list comprehension of serialized model list
        :param model_list:
        :return:
        """
        return [model_obj.serialize() for model_obj in model_list]


class Abstract(db.Model, Serializer):
    """
    Abstract base class for model objects

    adds default variables id, date_created
    and date_updated. Inherited by other models
    to avoid repetition.
    """
    __abstract__ = True
    __exclude__ = ['id']

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_updated = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class Employee(Abstract, UserMixin):
    """ Employee model class"""
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(EmailType, unique=True, nullable=False)
    password = db.Column(db.Text)

    def __repr__(self):
        return f'<Employee: {self.first_name} {self.last_name}>'


class Client(Abstract):
    """ Client model class"""
    name = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String(200))

    def __repr__(self):
        return f'<Client: {self.name}>'


class ProductArea(Abstract):
    """ ProductArea model class"""
    slug = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<ProductArea: {self.title}>'


class FeatureRequest(Abstract):
    """ FeatureRequest model class"""
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    client = db.relationship('Client')

    priority = db.Column(db.Integer, nullable=False)
    target_date = db.Column(db.Date, nullable=False)

    product_area_id = db.Column(db.Integer, db.ForeignKey('product_area.id'), nullable=False)
    product_area = db.relationship('ProductArea')

    def __repr__(self):
        return f'<FeatureRequest: Title - {self.title}, Priority - {self.priority}>'


# event listener for generating slug
event.listen(Client.name, 'set', generate_slug, retval=False)

# event listener for generating slug
event.listen(ProductArea.title, 'set', generate_slug, retval=False)
