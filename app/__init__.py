import os 
from flask import Flask
from app.extensions import db, bcrypt, login_manager, email
from flask_bcrypt import Bcrypt
from flask_mail import Mail



def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object("instance.config.Config")

    with app.app_context():
        db.init_app(app)
        login_manager.login_view = "login"
        login_manager.init_app(app)
        bcrypt = Bcrypt(app)
        email = Mail(app)
        
    
    
    from . import auth, dashboard, inbox
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(inbox.bp)

    return app

