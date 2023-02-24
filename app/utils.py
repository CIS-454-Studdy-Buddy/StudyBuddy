from app.models import *

def create_db():
    from app.extensions import db
    from app import create_app

    with create_app().app_context():
        db.create_all()
    
def seed_data():
   from app.extensions import db, bcrypt
   from app import create_app
   from app.models.user import User
   from app.models.course import Course

   with create_app().app_context():
        hashed_password = bcrypt.generate_password_hash("123456")
        new_user = User(first_name="Aaron", last_name="Alakkadan",  
                            username="aalakkad@syr.edu", password=hashed_password,
                            token="1234", is_verified=True)
        db.session.add(new_user)

        new_course = Course(name="Software Implementation", family="CIS",  
                            number="454")
        db.session.add(new_course)
        db.session.commit() 

        