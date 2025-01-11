from typing import Dict, Optional, List, Type, Any
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
import os, requests, json, random, string
from datetime import datetime, timedelta, timezone
from src import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from werkzeug.utils import secure_filename
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from cryptography.fernet import Fernet
from werkzeug.security import generate_password_hash, check_password_hash
import base64

import time
import os


def get_random_string(length=8):
    result_str = ''.join(random.choice('{}{}'.format('0123456789#@', string
        .ascii_letters)) for i in range(length))
    print(result_str)
    return result_str


class baseModel:
    id = db.Column(db.Integer, primary_key=True)
    date_create = db.Column(db.DateTime, default=datetime.utcnow)
    date_modify = db.Column(db.Integer, nullable=True)
    create_by = db.Column(db.Integer, nullable=True)
    modify_by = db.Column(db.Integer, nullable=True)

    def to_dict(self, data: Optional[Dict]=None):
        data = {'create_by': self.create_by, 'date_create': self.
            date_create, 'date_modify': self.date_modify, 'id': self.id,
            'modify_by': self.modify_by}
        return data

    def __init__(self, data=None):
        data = data or {}
        self.create_by = data.get('create_by', None)
        self.date_create = data.get('date_create', None)
        self.date_modify = data.get('date_modify', None)
        self.id = data.get('id', None)
        self.modify_by = data.get('modify_by', None)


class UserType(db.Model, baseModel):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), nullable=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    # user = db.relationship('User', backref='user_type_users')
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self=False, users=False):
        data = {'id': self.id, 'code': self.code, 'title': self.title,
            'description': self.description, 'created_on': self.timestamp.
            strftime('%Y-%m-%d %H:%M:%S')}
        if users:
            data['users'] = [user.to_dict(features=True) for user in self.users
                ]
        return data

    def from_dict(self, data, new_user_type=False):
        for field in ['title', 'description', 'code']:
            if field in data:
                setattr(self, field, data[field])


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(56), nullable=False)
    last_name = db.Column(db.String(56), nullable=False)
    telephone = db.Column(db.String(80), index=True, unique=True)
    phone = db.Column(db.String(25), index=True, unique=True)
    password_hash = db.Column(db.String(250))
    # last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    # status = db.Column(db.String(60), default='new')
    # login_token = db.Column(db.String(255))
    # timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # user_type_id = db.Column(db.Integer, db.ForeignKey('user_type.id'),
    #     nullable=True)
    # rule_id = db.Column(db.Integer, db.ForeignKey('rules.id'), nullable=True)
    date_pwd_generated = db.Column(db.DateTime(), default=datetime.utcnow)

    def to_dict(self, rules=False, user_type=False, password=False,
        partners=False):
        data = {'id': self.id, 'first_name': self.first_name, 'last_name':
            self.last_name, 'telephone': self.telephone, 'phone': self.phone,
            'last_seen': self.last_seen.strftime('%Y-%m-%d %H:%M:%S'),
            'created_on': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'status': self.status}
        # if user_type and self.user_type_id:
        #     val = UserType.query.get(self.user_type_id)
        #     if val:
        #         data['user_type'] = val.to_dict()
        #     else:
        #         data['user_type'] = {}
        # if password:
        #     data['default_password'] = password
        # if rules and self.rule_id:
        #     data['rule'] = Rules.query.get(self.rule_id).to_dict()
        return data

    def __init__(self, data=None):
        data = data or {}
        self.first_name = data.get('first_name', None)
        self.last_name = data.get('last_name', None)
        self.telephone = data.get('telephone', None)
        self.phone = data.get('phone', None)
        self.password_hash = generate_password_hash(data.get('password_hash', None))

    
        # self.password = generate_password_hash(data.get('password', None))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    # def from_dict(self, data, new_user=False):
    #     for field in ['first_name', 'last_name', 'telephone', 'phone', 'status',
    #         'api_user']:
    #         if field in data:
    #             setattr(self, field, data[field])
    #     if new_user and 'password' in data or 'password' in data:
    #         print(data['password'])
    #         self.set_password(data['password'])

    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)

    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)

    # def generate_auth_token(self, expiration=2592000):
    #     s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    #     return s.dumps({'id': self.id, 'telephone': self.telephone, 'state': self.
    #         status})

    # def get_reset_token(self, expires=2592000):
    #     # return jwt.encode({'reset_password': self.first_name, 'exp': time() + expiration},
    #     #                    key=os.getenv('SECRET_KEY_FLASK'))
    #     return jwt.encode({'reset_password': self.first_name, 'exp': time() + expires},
    #                        key=os.getenv('SECRET_KEY_FLASK'))
    
    # @staticmethod
    # def verify_reset_token(token):
    #     try:
    #         first_name = jwt.decode(token, key=os.getenv('SECRET_KEY_FLASK'))['reset_password']
    #         print(first_name)
    #     except Exception as e:
    #         print(e)
    #         return
    #     return User.query.filter_by(first_name=first_name).first()

    # @staticmethod
    # def verify_telephone(telephone):

    #     user = User.query.filter_by(telephone=telephone).first()

    #     return user

    # @staticmethod
    # def verify_auth_token(token):
    #     user = User.query.filter_by(login_token=token).first()
    #     if user:
    #         s = Serializer(current_app.config['SECRET_KEY'])
    #         s
    #         try:
    #             data = s.loads(token)
    #             print(data)
    #         except:
    #             return None
    #         return user
    #     else:
    #         return None

class Rules(db.Model, baseModel):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    default = db.Column(db.Boolean, default=False)
    # users = db.relationship('User', backref='rule_users')
    user_type_id = db.Column(db.Integer, db.ForeignKey('user_type.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self=False, users=False, user_type=False):
        data = {'id': self.id, 'title': self.title, 'description': self.
            description, 'default': self.default, 'created_on': self.
            timestamp.strftime('%Y-%m-%d %H:%M:%S')}
        if users:
            data['user'] = [user.to_dict() for user in self.users]
        if user_type and self.user_type_id:
            data['user_type'] = UserType.query.get(self.user_type_id).to_dict()
        return data

    def from_dict(self, data, new_rule=False):
        for field in ['title', 'description', 'timestamp', 'user_type_id',
            'default']:
            if field in data:
                setattr(self, field, data[field])

class Features(db.Model, baseModel):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), nullable=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    childs = db.relationship('Features')
    parent_id = db.Column(db.Integer, db.ForeignKey('features.id'))

    def to_dict(self, parent=False, childs=False):
        data = {'id': self.id, 'title': self.title, 'code': self.code,
            'description': self.description, 'created_on': self.timestamp.
            strftime('%Y-%m-%d %H:%M:%S')}
        if self.parent_id and parent:
            data['parent'] = Features.query.get(self.parent_id).to_dict()
        if childs:
            data['childs'] = [child.to_dict(childs=True) for child in self.
                childs]
        return data

    def from_dict(self, data, new_feature=False):
        for field in ['title', 'description', 'timestamp', 'parent_id', 'code'
            ]:
            if field in data:
                setattr(self, field, data[field])

# Repetiteur
class Repetiteurs(db.Model, baseModel):
    nomcomplet = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(80), index=True, nullable=True)
    contactWhats = db.Column(db.String(10), nullable=True)
    lieu = db.Column(db.String(25), nullable=True)
    quartHab = db.Column(db.String(25), nullable=True)
    classPrim = db.Column(db.String(100), nullable=True)
    classSecond = db.Column(db.String(150), nullable=True)
    annExp = db.Column(db.String(2), nullable=True)
    nivEtud = db.Column(db.String(10), nullable=True)
    passwordR = db.Column(db.String(250))
    image = db.Column(db.Text, nullable=True)

    def to_dict(self, data: Optional[Dict]=None):
        data = {'id': self.id, 'nomcomplet': self.nomcomplet, 'email': self.email, 'contactWhats':
            self.contactWhats, 'lieu': self.lieu, 'quartHab': self.quartHab, 'classPrim': self.classPrim,
            'classSecond': self.classSecond, 'annExp': self.annExp, 'nivEtud': self.nivEtud, 'image': self.image}
        return data

    def __init__(self, data=None):
        data = data or {}
        self.nomcomplet = data.get('nomcomplet', None)
        self.email = data.get('email', None)
        self.contactWhats = data.get('contactWhats', None)
        self.lieu = data.get('lieu', None)
        self.quartHab = data.get('quartHab', None)
        self.classPrim = data.get('classPrim', None)
        self.classSecond = data.get('classSecond', None)
        self.annExp = data.get('annExp', None)
        self.nivEtud = data.get('nivEtud', None)
        self.passwordR = generate_password_hash(data.get('passwordR'))
        self.image = data.get('image', None)

    def set_password(self, password):
        self.passwordR = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwordR, password)

    @staticmethod
    def verify_auth_token(token):
        user = User.query.filter_by(login_token=token).first()
        if user:
            return user
        else:
            return None

class Parents(db.Model, baseModel):
    nomcomplet_parent = db.Column(db.String(30), nullable=True)
    telephone = db.Column(db.String(10), nullable=True)
    lieu = db.Column(db.String(25), nullable=True)
    quartHab = db.Column(db.String(25), nullable=True)
    password_hash = db.Column(db.String(250))

    def to_dict(self, data: Optional[Dict]=None):
        data = {'id' : self.id,
                'nomcomplet_parent': self.nomcomplet_parent,
                'telephone': self.telephone,
                'lieu': self.lieu, 
                'quartHab': self.quartHab,
                'password_hash': self.password_hash,
                }
        return data
    
    def __init__(self, data=None):
        data = data or {}
        self.nomcomplet_parent = data.get('nomcomplet_parent', None)
        self.telephone = data.get('telephone', None)
        self.lieu = data.get('lieu', None)
        self.quartHab = data.get('quartHab', None)
        self.password_hash = generate_password_hash(data.get('password_hash', None))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # def from_dict(self, data, new_feature=False):
    #     for field in ['nomcomplet_parent', 'telephone', 'telephone']:
    #         if field in data:
    #             setattr(self, field, data[field])
