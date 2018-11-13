from flask_wtf import FlaskForm
from wtforms_alchemy import ModelForm, ModelFieldList
from wtforms.fields import StringField, PasswordField, BooleanField, TextAreaField, IntegerField, FormField
from wtforms.validators import Email, DataRequired, Optional

from application import models


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], filters=[lambda x: x or ''])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me', validators=[Optional()])


class FeatureRequestForm(ModelForm):
    class Meta:
        model = models.FeatureRequest



