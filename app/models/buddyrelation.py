from app.extensions import db
from app.models.user import User
from app.models.course import Course, Subject
from app.models.studyinterest import StudyInterest
from sqlalchemy.orm import relationship
from datetime import datetime

MAX_UPLOADS_PER_DAY = 20

class BuddyRelation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buddy_sender = db.Column(db.Integer, db.ForeignKey("user.id"))
    buddy_receiver = db.Column(db.Integer, db.ForeignKey("user.id"))
    study_interest_id = db.Column(db.Integer, db.ForeignKey("study_interest.id"))
    invitation_status = db.Column(db.String(1), nullable=False, default = 'N')
    upload_count_sender = db.Column(db.Integer, nullable=False, default = 0)
    upload_count_receiver = db.Column(db.Integer, nullable=False, default = 0)
    reset_upload_date_sender = db.Column(db.Date, nullable=True)
    reset_upload_date_receiver = db.Column(db.Date, nullable=True)

    sender = relationship("User", foreign_keys=[buddy_sender])
    receiver = relationship("User", foreign_keys=[buddy_receiver])
    study_interest = relationship("StudyInterest")
    
    def get_buddy(self, current_user_id):
        if current_user_id == self.sender.username:
            return self.receiver
        else:
            return self.sender
        
    def can_user_upload(self, current_user_id):
        if current_user_id == self.sender.username:
            if self.reset_upload_date_sender is not None:
                if self.reset_upload_date_sender < datetime.today().date():
                    self.upload_count_sender = 0
                    self.reset_upload_date_sender = datetime.today().date()
                    db.session.commit()
                    return True
                elif self.reset_upload_date_sender == datetime.today().date():
                    if self.upload_count_sender >= MAX_UPLOADS_PER_DAY:
                        return False
                    else:
                        return True
                else:
                    self.reset_upload_date_sender = datetime.today().date()
                    db.session.commit()
                    return True
            else:
                self.reset_upload_date_sender = datetime.today().date()
                db.session.commit()
                return True
        elif current_user_id == self.receiver.username:
            if self.reset_upload_date_receiver is not None:
                if self.reset_upload_date_receiver < datetime.today().date():
                    self.upload_count_receiver = 0
                    self.reset_upload_date_receiver = datetime.today().date()
                    db.session.commit()
                    return True
                elif self.reset_upload_date_receiver == datetime.today().date():
                    if self.upload_count_receiver >= MAX_UPLOADS_PER_DAY:
                        return False
                    else:
                        return True
                else:
                    self.reset_upload_date_receiver = datetime.today().date()
                    db.session.commit()
                    return True
            else:
                self.reset_upload_date_receiver = datetime.today().date()
                db.session.commit()
                return True
        else:
            return False

    def __repr__(self):
        return f"<BuddyRelation {self.id}, {self.study_interest_id}>"