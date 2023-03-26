import os 
from flask import Flask
#from . import findstudybuddy
from app.extensions import db, bcrypt, login_manager, email
from flask_bcrypt import Bcrypt
from flask_mail import Mail



def create_app(test_config=None):
    app = Flask(__name__)
    if test_config:
        app.config.from_object("instance.config.TestConfig")
    else: 
        app.config.from_object("instance.config.Config")

    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024     # 5MB

    with app.app_context():
        db.init_app(app)
        login_manager.login_view = "login"
        login_manager.init_app(app)
        bcrypt = Bcrypt(app)
        email = Mail(app)
        
    
    
    from . import auth, dashboard, findstudybuddy, subjectselection, materialsupload, materialsview, rate, viewratings, profile, removebuddy
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(findstudybuddy.bp)
    app.register_blueprint(subjectselection.bp)
    app.register_blueprint(materialsupload.bp)
    app.register_blueprint(materialsview.bp)
    app.register_blueprint(rate.bp)
    app.register_blueprint(viewratings.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(removebuddy.bp)

    
    return app

