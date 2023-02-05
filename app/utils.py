from app.models import *

def create_db():
    from app.extensions import db
    from app import create_app

    with create_app().app_context():
        db.create_all()
        