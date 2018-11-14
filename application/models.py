import datetime

# import flask application
from flask import current_app

# import usermixin
from flask_login import UserMixin

# Import SQLAlchemy
from sqlalchemy.inspection import inspect
from sqlalchemy import event
from flask_sqlalchemy import SQLAlchemy

# import slugify
from slugify import slugify


def generate_slug(target, value, oldvalue, initiator):
    if value and (not target.slug or value != oldvalue):
        target.slug = slugify(value)


class Serializer(object):

    def serialize(self):
        """
        serialize model object
        :return:
        """
        output = dict()
        for c in inspect(self).attrs.keys():
            if c not in getattr(self, '__exclude__'):
                # retrieve attribute not excluded
                if isinstance(getattr(self, c), datetime.time):
                    output[c] = getattr(self, c).isoformat()
                elif isinstance(getattr(self, c), db.Model):
                    output[c] = getattr(self, c).serialize()
                else:
                    output[c] = getattr(self, c)

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

    # Define database object
    db = SQLAlchemy()
    db.init_app(current_app)

    class Abstract(db.Model, Serializer):
        __abstract__ = True
        __exclude__ = ['id']

        id = db.Column(db.Integer, primary_key=True)
        date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
        date_updated = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


    class Employee(Abstract, UserMixin):
        first_name = db.Column(db.String(255), nullable=False)
        last_name = db.Column(db.String(255), nullable=False)
        email = db.Column(db.String(200), unique=True, nullable=False)
        password = db.Column(db.Text)

        def __repr__(self):
            return f'<Employee: {self.first_name} {self.last_name}>'


    class Client(Abstract):
        name = db.Column(db.Text, nullable=False)
        slug = db.Column(db.String(200))

        def __repr__(self):
            return f'<Client: {self.name}>'

    # event listener for generating slug
    event.listen(Client.name, 'set', generate_slug, retval=False)


    class ProductArea(Abstract):
        slug = db.Column(db.String(255), nullable=False)
        title = db.Column(db.String(255), nullable=False)

        def __repr__(self):
            return f'<ProductArea: {self.title}>'

        # @staticmethod
        # def generate_slug(target, value, oldvalue, initiator):
        #     if value and (not target.slug or value != oldvalue):
        #         target.slug = slugify(value)

    # event listener for generating slug
    event.listen(ProductArea.title, 'set', generate_slug, retval=False)


    class FeatureRequest(Abstract):
        title = db.Column(db.String(255), nullable=False)
        description = db.Column(db.Text, nullable=False)
        client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
        client = db.relationship('Client')

        client_priority = db.Column(db.Integer, nullable=False)
        target_date = db.Column(db.Date, nullable=False)

        product_area_id = db.Column(db.Integer, db.ForeignKey('product_area.id'), nullable=False)
        product_area = db.relationship('ProductArea')

        def __repr__(self):
            return f'<FeatureRequest: Title - {self.title}, Priority - {self.client_priority}>'
