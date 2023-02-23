'''
Author: Aaron Alakkadan, Matt Faiola, Talal Hakki
'''

from app.extensions import db
from flask_login import UserMixin
from datetime import datetime

'''
This is the user class model which we inherits from the db.Model class. This represents the user table.    
'''
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False, default = '')
    last_name  = db.Column(db.String(50), nullable=False, default = '')
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    token = db.Column(db.String(20), nullable=True, unique=True)
    is_verified = db.Column(db.Boolean, nullable=False, default=False)
    phone_number = db.Column(db.String(20), nullable=True, unique=True)
    about_me = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    def __repr__(self):
        return f"<User {self.id}>"

