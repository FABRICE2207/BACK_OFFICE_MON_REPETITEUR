from flask import Blueprint

api = Blueprint('api', __name__,static_url_path='/app/static')

from . import views, tokens