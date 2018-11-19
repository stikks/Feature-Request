"""
application forms
"""
from wtforms import Form
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, IntegerField, DateField
from wtforms.validators import Email, DataRequired, Optional


class LoginForm(FlaskForm):
    """
    Login Form
    """
    # filter prevents form field from being None
    email = StringField('Email', validators=[DataRequired(), Email()], filters=[lambda x: x or ''])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me', validators=[Optional()])


class FeatureRequestFlaskForm(FlaskForm):
    """ FeatureRequest Form """
    # current max value of feature request priority

    # filter prevents form field from being None
    title = StringField('Title', validators=[DataRequired()], filters=[lambda x: x or ''])

    # filter prevents form field from being None
    description = StringField('Description', validators=[DataRequired()], filters=[lambda x: x or ''])

    product_area_id = IntegerField('Product Area', validators=[DataRequired()])
    client_id = IntegerField('Client', validators=[DataRequired()])
    priority = IntegerField('Priority', validators=[DataRequired()])
    target_date = DateField('Target Date', validators=[DataRequired()])


class FeatureRequestForm(Form):
    """ FeatureRequest Form """
    # current max value of feature request priority

    # filter prevents form field from being None
    title = StringField('Title', validators=[DataRequired()], filters=[lambda x: x or ''])

    # filter prevents form field from being None
    description = StringField('Description', validators=[DataRequired()], filters=[lambda x: x or ''])

    product_area_id = IntegerField('Product Area', validators=[DataRequired()])
    client_id = IntegerField('Client', validators=[DataRequired()])
    priority = IntegerField('Priority', validators=[DataRequired()])
    target_date = DateField('Target Date', validators=[DataRequired()])


class EmployeeForm(Form):
    """Employee Form"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])


class ClientForm(Form):
    """Client Form"""
    name = StringField('Name', validators=[DataRequired()])


class ProductAreaForm(Form):
    """ProductArea Form"""
    title = StringField('Name', validators=[DataRequired()])
