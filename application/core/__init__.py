from flask import Blueprint

core = Blueprint('core', __name__, template_folder='templates', static_folder='static')

from . import views, ajax_views