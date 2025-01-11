from flask import Blueprint

dash = Blueprint('dashboard', __name__)

from . import views
