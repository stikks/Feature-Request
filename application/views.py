from flask import current_app, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required

from . import forms
from .services import account, client, feature


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


@current_app.route('/login', methods=['GET', 'POST'])
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

    form = forms.LoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        data = form.data.copy()
        data.pop('csrf_token')
        employee = account.login(**data)

        if employee:
            return redirect(url_for('index'))

        flash(u'Invalid email/password combination', 'error')

    return render_template('login.html', **locals())


@current_app.route('/logout', methods=['GET'])
@login_required
def logout():
    """
    logout route

    redirects to login route on successful logout
    :return:
    """
    account.logout_user()
    return redirect(url_for('login'))


@current_app.route('/', methods=['GET'])
@current_app.route('/clients', methods=['GET'])
@login_required
def index():
    """
    clients list view

    shows list of registered clients. shows empty table
    if none found
    :return:
    """
    return render_template('index.html', **locals())


@current_app.route('/clients/<client_slug>/feature-requests', methods=['GET'])
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

    return render_template('feature_requests/list.html', **locals())


@current_app.route('/clients/<client_slug>/feature-requests/new', methods=['GET'])
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

    product_areas = feature.ProductAreaService.objects_all()

    form = forms.FeatureRequestForm(client_id=obj_client.id)

    return render_template('feature_requests/new.html', **locals())

