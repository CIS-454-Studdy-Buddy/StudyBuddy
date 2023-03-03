from app.extensions import db
'''
Author: Aaron Alakkadan 
'''
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_code = db.Column(db.String(10), nullable=False)
    course_number = db.Column(db.String(10), nullable=False, default = '')
    course_name = db.Column(db.String(100), nullable=False, default = '')


    def __repr__(self):
        return f"<Course {self.id}, {self.course_name}>"

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_code = db.Column(db.String(10), nullable=False, unique=True, default = '')
    subject_name = db.Column(db.String(100), nullable=False, default = '')

    def __repr__(self):
        return f"<Subject {self.id}, {self.subject_code,}, {self.subject_name}>"
