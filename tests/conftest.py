import pytest
from app import create_app, db
from app.models import *
from app.utils import import_courses, import_subject_code, seed_test_data

@pytest.fixture()
def app():
    app = create_app("sqlite:///debug.db")
    app.config["WTF_CSRF_ENABLED"] = False
    with app.app_context():
        db.create_all()
        import_subject_code('instance/sortedCode.csv')
        import_courses('instance/sortedCourse.csv')
        #seed_test_data()
        
    
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()