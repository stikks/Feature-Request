from flask import current_app, render_template, request, redirect, url_for
from flask_login import login_required

from . import forms
from .services import account, client, feature


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
        pass


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


@current_app.route('/clients', methods=['GET'])
@login_required
def client_list():
    """
    clients list view

    shows list of registered clients. shows empty table
    if none found
    :return:
    """
    clients = client.clients_all()
    return render_template('clients/list.html', **locals())


@current_app.route('/', methods=['GET'])
@current_app.route('/feature-requests', methods=['GET'])
@login_required
def feature_request_list():
    """
    feature requests list view

    shows list of feature requests. shows empty table
    if none found
    :return:
    """
    feature_requests = feature.feature_requests_all()
    return render_template('feature_requests/list.html', **locals())


@current_app.route('/feature-requests/new', methods=['POST'])
@login_required
def feature_request_create():
    """
    feature requests list view

    shows list of feature requests. shows empty table
    if none found
    :return:
    """
    feature_requests = feature.feature_requests_all()
    return render_template('feature_requests/new.html', **locals())

