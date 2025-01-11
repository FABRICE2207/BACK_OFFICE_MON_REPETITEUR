from flask import jsonify, request
from src import db
from src.api import api
from src.api.authentification import basic_auth
from flask_httpauth import HTTPTokenAuth
from src.models import User
from src.api.errors import error_response, unauthorized
from flask_cors import CORS,cross_origin
from . import api
# from .authentication import basic_auth
from flask import g

token_auth = HTTPTokenAuth(scheme='Bearer', header='Authorization')

CORS(api,  resources={r"*": {"origins": "*"}})
@token_auth.verify_token
def verify_token(token):
    token = request.authorization.token
    return Ouvriers.verify_auth_token(token) if token else None

@token_auth.error_handler
def token_auth_error():
    return unauthorized('Vous n\'êtes pas autorisé à effectuer cette action')

@api.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().generate_auth_token()
    g.token = token
    db.session.commit()
    return jsonify({'token': token, 'ouvrier' : basic_auth.current_user().to_dict()})
