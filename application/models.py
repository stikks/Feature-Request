"""
application models
"""
import datetime

# import flask application
from flask import current_app

# import usermixin
from flask_login import UserMixin

# Import SQLAlchemy
from sqlalchemy.inspection import inspect
from sqlalchemy import event

# import slugify
from slugify import slugify


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
                elif isinstance(getattr(self, key), DB.Model):
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


with current_app.app_context():

    DB = current_app.db

    class Abstract(DB.Model, Serializer):
        """ 
        Abstract base class for model objects
        
        adds default variables id, date_created
        and date_updated. Inherited by other models
        to avoid repetition.
        """
        __abstract__ = True
        __exclude__ = ['id']

        id = DB.Column(DB.Integer, primary_key=True)
        date_created = DB.Column(DB.DateTime, default=DB.func.current_timestamp())
        date_updated = DB.Column(DB.DateTime, default=DB.func.current_timestamp(), onupdate=DB.func.current_timestamp())


    class Employee(Abstract, UserMixin):
        """ Employee model class"""
        first_name = DB.Column(DB.String(255), nullable=False)
        last_name = DB.Column(DB.String(255), nullable=False)
        email = DB.Column(DB.String(200), unique=True, nullable=False)
        password = DB.Column(DB.Text)

        def __repr__(self):
            return f'<Employee: {self.first_name} {self.last_name}>'


    class Client(Abstract):
        """ Client model class"""
        name = DB.Column(DB.Text, nullable=False)
        slug = DB.Column(DB.String(200))

        def __repr__(self):
            return f'<Client: {self.name}>'

    # event listener for generating slug
    event.listen(Client.name, 'set', generate_slug, retval=False)


    class ProductArea(Abstract):
        """ ProductArea model class"""
        slug = DB.Column(DB.String(255), nullable=False)
        title = DB.Column(DB.String(255), nullable=False)

        def __repr__(self):
            return f'<ProductArea: {self.title}>'

    # event listener for generating slug
    event.listen(ProductArea.title, 'set', generate_slug, retval=False)


    class FeatureRequest(Abstract):
        """ FeatureRequest model class"""
        title = DB.Column(DB.String(255), nullable=False)
        description = DB.Column(DB.Text, nullable=False)
        client_id = DB.Column(DB.Integer, DB.ForeignKey('client.id'), nullable=False)
        client = DB.relationship('Client')

        priority = DB.Column(DB.Integer, nullable=False)
        target_date = DB.Column(DB.Date, nullable=False)

        product_area_id = DB.Column(DB.Integer, DB.ForeignKey('product_area.id'), nullable=False)
        product_area = DB.relationship('ProductArea')

        def __repr__(self):
            return f'<FeatureRequest: Title - {self.title}, Priority - {self.priority}>'
