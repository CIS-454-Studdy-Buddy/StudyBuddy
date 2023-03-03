from app.models import *
from app.models.user import User
from app.models.studyinterest import StudyInterest
from app.models.buddyrelation import BuddyRelation
from app.models.course import Course, Subject
from app.extensions import db
import os
import csv


def import_courses(file_path):
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            model_instance = Course(subject_code=row[0], course_number=row[1], course_name=row[2])
            db.session.add(model_instance)
        db.session.commit()

def import_subject_code(file_path):
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            model_instance = Subject(subject_code=row[0], subject_name=row[1])
            db.session.add(model_instance)
        db.session.commit()

def create_db():
    from app import create_app

    #tables = ['course', 'subject', 'studyinterest', 'user']
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
                            token="1234", is_verified=True, phone_number="3155777555", about_me="I am a student at Syracuse University")
        new_user2 = User(first_name="Matt", last_name="Faiola",  
                            username="mjfaiola@syr.edu", password=hashed_password,
                            token="234234", is_verified=True, phone_number="3155555555", about_me="I am a student at Syracuse University")
        new_user3 = User(first_name="Talal", last_name="Hakki",  
                            username="thakki@syr.edu", password=hashed_password,
                            token="4567", is_verified=True, phone_number="3151231234", about_me="I am a student at Syracuse University")
        db.session.add(new_user)
        db.session.add(new_user2)
        db.session.add(new_user3)
        db.session.commit()
        