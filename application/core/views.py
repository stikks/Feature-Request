"""
application routes
"""
from flask import current_app, render_template, request, redirect, url_for, flash, abort, session
from flask_login import login_required

from application import forms
from application.core.services import client, feature
from application.core.services import account

from . import core


@current_app.errorhandler(404)
def not_found(error):
    """
    hamdle 404 errors
    :param error:
    :return:
    """
    return render_template('404.html'), 404


@current_app.login_manager.user_loader
def load_user(employee_id):
    """
    returns user object if session authenticated
    else None
    :param employee_id:
    :return:
    """
    return account.EmployeeService.objects_get(employee_id)


@core.route('/login', methods=['GET', 'POST'])
def login():
    """
    login route

    shows login form on GET request.
    attempts user authentication on POST request, using
    the credentials in request body. redirects to homepage
    if authentication successful, else it reloads login form
    passing form errors to it.

    :return:
    """
    title = 'Sign In'
    form = forms.LoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        data = form.data.copy()

        data.pop('csrf_token')
        employee = account.login(**data)

        if employee:
            return redirect(url_for('core.index'))

        flash(u'Invalid email/password combination', 'error')

    return render_template('login.html', **locals())


@core.route('/logout', methods=['GET'])
@login_required
def logout():
    """
    logout route

    redirects to login route on successful logout
    :return:
    """
    account.logout_user()
    return redirect(url_for('core.login'))


@core.route('/', methods=['GET'])
@core.route('/clients', methods=['GET'])
@login_required
def index():
    """
    clients list view

    shows list of registered clients. shows empty table
    if none found
    :return:
    """
    title = 'Home'

    print(g.user)

    return render_template('index.html', **locals())


@core.route('/clients/<client_slug>/feature-requests', methods=['GET'])
@login_required
def feature_requests_list(client_slug):
    """
    feature requests list view

    shows list of feature requests. shows empty table
    if none found
    :return:
    """
    obj_client = client.ClientService.objects_filter(**dict(slug=client_slug))

    if not obj_client:
        raise abort(404)
    
    title = f'{obj_client.name}'

    return render_template('feature_requests/list.html', **locals())


@core.route('/clients/<client_slug>/feature-requests/new', methods=['GET', 'POST'])
@login_required
def feature_request_create(client_slug):
    """
    feature requests create view

    shows list of feature requests. shows empty table
    if none found
    :return:
    """
    obj_client = client.ClientService.objects_filter(**dict(slug=client_slug))

    if not obj_client:
        raise abort(404)

    title = f'{obj_client.name}'

    product_areas = feature.ProductAreaService.objects_all()

    model_class = feature.FeatureRequestService.model_class
    db = current_app.db

    sub = db.session.query(db.func.max(model_class.priority).label('ml')).subquery()
    feature_request = db.session.query(model_class).join(sub, sub.c.ml == model_class.priority).one()
    max_value = feature_request.priority + 1 if feature_request else 1

    form = forms.FeatureRequestForm()

    if request.method == 'POST' and form.validate_on_submit():
        data = form.data.copy()
        data.pop('csrf_token')
        feature_request = feature.FeatureRequestService.objects_new(**data)

        if feature_request:
            flash('successfully created feature request', 'success')
            return redirect(url_for('core.feature_requests_list', client_slug=obj_client.slug))

    return render_template('feature_requests/new.html', **locals())
