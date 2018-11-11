import datetime

# import flask application
from flask import current_app

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect


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
    db = SQLAlchemy(current_app)

    class Abstract(db.Model, Serializer):
        __abstract__ = True
        __exclude__ = ['id']

        id = db.Column(db.Integer, primary_key=True)
        date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
        date_updated = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


    class Employee(Abstract):
        first_name = db.Column(db.String(255), nullable=False)
        last_name = db.Column(db.String(255), nullable=False)
        email = db.Column(db.String(200), unique=True, nullable=False)

        def __repr__(self):
            return f'<Employee: {self.first_name} {self.last_name}>'


    class Client(Abstract):
        first_name = db.Column(db.String(255), nullable=False)
        last_name = db.Column(db.String(255), nullable=False)
        email = db.Column(db.String(200), unique=True, nullable=False)

        def __repr__(self):
            return f'<Client: {self.first_name} {self.last_name}'

    class ProductArea(Abstract):
        code = db.Column(db.String(255), nullable=False)
        title = db.Column(db.String(255), nullable=False)

        def __repr__(self):
            return f'<ProductArea: {self.title}>'


    class FeatureRequest(Abstract):
        title = db.Column(db.String(255), nullable=False)
        description = db.Column(db.Text, nullable=False)
        client = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
        client_priority = db.Column(db.Integer, nullable=False)
        target_date = db.Column(db.Date, nullable=False)
        product_area = db.Column(db.Integer, db.ForeignKey('product_area.id'), nullable=False)

        def __repr__(self):
            return f'<FeatureRequest: Title - {self.title}, Priority - {self.client_priority}>'
