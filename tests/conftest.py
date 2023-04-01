# Author: Aaron Alakkadan 
import pytest
from app import create_app, db
from app.models import *
from app.utils import import_courses, import_subject_code, seed_test_data

'''
The function app is used to create the test database along with importing the corresponding courses in order to test.
'''
@pytest.fixture()
def app():
    app = create_app("sqlite:///debug.db")
    app.config["WTF_CSRF_ENABLED"] = False
    with app.app_context():
        db.create_all()
        import_subject_code('instance/sortedCode.csv')
        import_courses('instance/sortedCourse.csv')
            
    yield app

'''
The function client is the instance used for pytest when sending post or get data to and from the website. 
'''
@pytest.fixture()
def client(app):
    return app.test_client()

