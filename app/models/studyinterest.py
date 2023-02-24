from app.extensions import db
from app.models.user import User
from app.models.course import Courses, SubjectCode
from sqlalchemy.orm import relationship

class StudyInterest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
    proAns1 = db.Column(db.Integer, nullable=False, default=0)
    proAns2 = db.Column(db.Integer, nullable=False, default=0)
    proAns3 = db.Column(db.Integer, nullable=False, default=0)
    proScore = db.Column(db.Numeric(precision=2, scale=2), nullable=False)


    user = relationship("User")
    course = relationship("Courses")

    def __repr__(self):
        return f"<StudyInterest {self.id}>"
