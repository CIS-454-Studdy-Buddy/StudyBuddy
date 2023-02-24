from app.models import *
from app.models.user import User
from app.models.studyinterest import StudyInterest
from app.models.course import Courses, SubjectCode
from app.extensions import db
import os
import csv


def import_courses(file_path):
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            model_instance = Courses(subject_code=row[0], course_number=row[1], course_name=row[2])
            db.session.add(model_instance)
        db.session.commit()

def import_subject_code(file_path):
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            model_instance = SubjectCode(subject_code=row[0], subject_name=row[1])
            db.session.add(model_instance)
        db.session.commit()

def create_db():
    from app import create_app

    #tables = ['courses', 'subjectcode', 'studyinterest', 'user']
    #tables_exist = db.engine.dialect.has_table(db.engine, tables)

    if os.path.isfile('instance/database.db'):
        os.remove('instance/database.db')
        with create_app().app_context():
            db.create_all()
            import_subject_code('instance/sortedCode.csv')
            import_courses('instance/sortedCourse.csv')
        print("New Database Created")
    else:
        print("The file does not exist")
        with create_app().app_context():
            db.create_all()
        print("Database Created")


def seed_data():
   from app.extensions import db, bcrypt
   from app import create_app

   with create_app().app_context():
        hashed_password = bcrypt.generate_password_hash("123456")
        new_user = User(first_name="Aaron", last_name="Alakkadan",  
                            username="aalakkad@syr.edu", password=hashed_password,
                            token="1234", is_verified=True)
        new_user2 = User(first_name="Matt", last_name="Faiola",  
                            username="mjfaiola@syr.edu", password=hashed_password,
                            token="1234", is_verified=True)
        db.session.add(new_user)
        db.session.add(new_user2)
        db.session.commit()
        