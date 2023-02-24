from app.extensions import db

class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_code = db.Column(db.String(10), nullable=False, default = '')
    course_number = db.Column(db.String(10), nullable=False, default = '')
    course_name = db.Column(db.String(100), nullable=False, default = '')

    def __repr__(self):
        return f"<Courses {self.id}, {self.course_name}>"

class SubjectCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_code = db.Column(db.String(10), nullable=False, default = '')
    subject_name = db.Column(db.String(100), nullable=False, default = '')

    def __repr__(self):
        return f"<SubjectCode {self.id}, {self.subject_code,}, {self.subject_name}>"
