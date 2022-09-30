import imp
import os
from werkzeug.utils import secure_filename
from pickletools import read_uint1
from flask import Flask
from flask_login import LoginManager
from flaskr.models import setup_db, Users
from dotenv import load_dotenv
from flask_cors import CORS

from flask_migrate import Migrate
from flask_mysqldb import MySQL


load_dotenv()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.secret_key = os.getenv("APP_SECRET")
    setup_db(app)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization, true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, POST, DELETE, PATCH, OPTIONS"
        )
        return response

    # blueprint for auth routes in app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

   