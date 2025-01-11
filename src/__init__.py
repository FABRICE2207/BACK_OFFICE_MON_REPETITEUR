from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
from config import config
from flask_login import LoginManager
import os
# from werkzeug.utils import secure_filename

db = SQLAlchemy()
migrate = Migrate()
# login = LoginManager()
# login.login_view = 'auth.login'
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
jwt = JWTManager()
mail = Mail()

# # # Define allowed files
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def create_app(config_name='development'):
    app = Flask(__name__)

    from src.models import User
    absolute_path = os.path.dirname(__file__)
    UPLOAD_FOLDER = os.path.join(absolute_path,'static','images')
    ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])
    
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    
    CORS(app, resources={r"*": {"Access-Control-Allow-Origin": "*"}})
    if hasattr(config_name,'data'):
        config_name = os.environ.get('FLASK_CONFIG')
   
    app.config.from_object(config[config_name])
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    # Configure upload folder for Flask application
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
    # config[config_name].init_app(app)
    db.init_app(app)
    # login.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app,db)
    jwt.init_app(app)
    mail.init_app(app)
    # sess.init_app(app)
   

    from .dashboard import dash as dash_bleuprint
    app.register_blueprint(dash_bleuprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .api import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix="/api")

    # from .screen.screen import screen_bp as screen_blueprint
    # app.register_blueprint(screen_blueprint, url_prefix="/screen")

    return app
