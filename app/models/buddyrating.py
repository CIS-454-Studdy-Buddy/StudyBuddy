import datetime
from app.extensions import db
from app.models.user import User
from app.models.course import Course, Subject
from app.models.studyinterest import StudyInterest
from app.models.buddyrelation import BuddyRelation
from sqlalchemy.orm import relationship

class BuddyRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buddy_sender = db.Column(db.Integer, db.ForeignKey("user.id"))
    buddy_receiver = db.Column(db.Integer, db.ForeignKey("user.id"))
    rating_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    is_score_improved = db.Column(db.Boolean, nullable=False)
    is_gained_knowledge = db.Column(db.Boolean, nullable=False)
    comment = db.Column(db.Text, nullable=False, default = '')
    is_survey_completed = db.Column(db.Boolean, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    sender = relationship("User", foreign_keys=[buddy_sender])
    receiver = relationship("User", foreign_keys=[buddy_receiver])
