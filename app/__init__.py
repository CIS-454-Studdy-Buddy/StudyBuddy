import os 
from flask import Flask
from app.extensions import db, bcrypt, login_manager
from flask_bcrypt import Bcrypt


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object("instance.config.Config")

    with app.app_context():
        db.init_app(app)
        login_manager.login_view = "login"
        login_manager.init_app(app)
        bcrypt = Bcrypt(app)
    
    
    from . import auth, dashboard
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)

    return app

