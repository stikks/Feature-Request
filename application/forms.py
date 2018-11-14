from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, IntegerField, DateField
from wtforms.validators import Email, DataRequired, Optional, NumberRange

from application import models


class LoginForm(FlaskForm):
    # filter prevents form field from being None
    email = StringField('Email', validators=[DataRequired(), Email()], filters=[lambda x: x or ''])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me', validators=[Optional()])


class FeatureRequestForm(FlaskForm):

    # current max value of feature request priority
    value = models.db.session.query(models.FeatureRequest.priority).scalar()
    max_value = 1 if value is None else value + 1

    # filter prevents form field from being None
    title = StringField('Title', validators=[DataRequired()], filters=[lambda x: x or ''])

    # filter prevents form field from being None
    description = StringField('Description', validators=[DataRequired()], filters=[lambda x: x or ''])

    product_area_id = IntegerField('Product Area', validators=[DataRequired()])
    client_id = IntegerField('Client', validators=[DataRequired()])
    priority = IntegerField('Priority', validators=[DataRequired(), NumberRange(min=1, max=max_value)])
    target_date = DateField('Target Date', validators=[DataRequired()])