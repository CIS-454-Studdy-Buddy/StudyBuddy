from app.extensions import db
from app.models.user import User
from app.models.course import Course, Subject
from app.models.studyinterest import StudyInterest
from sqlalchemy.orm import relationship

class BuddyRelation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buddy_sender = db.Column(db.Integer, db.ForeignKey("user.id"))
    buddy_receiver = db.Column(db.Integer, db.ForeignKey("user.id"))
    study_interest_id = db.Column(db.Integer, db.ForeignKey("study_interest.id"))
    invitation_status = db.Column(db.String(1), nullable=False, default = 'N')

    sender = relationship("User", foreign_keys=[buddy_sender])
    receiver = relationship("User", foreign_keys=[buddy_receiver])
    study_interest = relationship("StudyInterest")
    
    def get_buddy(self, current_user_id):
        if current_user_id == self.sender.username:
            return self.receiver
        else:
            return self.sender


    def __repr__(self):
        return f"<BuddyRelation {self.id}, {self.study_interest_id}>"