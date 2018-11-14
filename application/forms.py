from flask_wtf import FlaskForm
from wtforms_alchemy import ModelForm, ModelFieldList
from wtforms.fields import StringField, PasswordField, BooleanField, TextAreaField, IntegerField, FormField, DateField
from wtforms.validators import Email, DataRequired, Optional

from application import models


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], filters=[lambda x: x or '']) # filter prevents form field from being None
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me', validators=[Optional()])


class FeatureRequestForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], filters=[lambda x: x or '']) # filter prevents form field from being None
    description = StringField('Description', validators=[DataRequired()], filters=[lambda x: x or '']) # filter prevents form field from being None
    product_area_id = IntegerField('Product Area', validators=[DataRequired()])
    client_id = IntegerField('Client', validators=[DataRequired()])
    client_priority = IntegerField('Client Priority', validators=[DataRequired()])
    target_date = DateField('Target Date', validators=[DataRequired()])

