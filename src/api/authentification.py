from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
# from src.models import Ouvriers
from src.api.errors import error_response, unauthorized
from flask import g
basic_auth = HTTPBasicAuth()

# token_auth = HTTPTokenAuth()

# @basic_auth.verify_password
# def verify_password(username, password):
    
#     ouvrier = Ouvriers.query.filter_by(email=username).first()
#     if  ouvrier and ouvrier.check_password(password):
#         return ouvrier
   

# @basic_auth.error_handler
# def basic_auth_error():
#     return unauthorized('Mot de passe ou email invalide'),401