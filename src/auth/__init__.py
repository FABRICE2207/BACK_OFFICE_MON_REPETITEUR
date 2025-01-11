from flask import Blueprint

auth = Blueprint('auth', __name__,static_url_path='/app/static')

from . import views
