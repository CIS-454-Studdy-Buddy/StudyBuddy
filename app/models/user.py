from app.extensions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False, default = '')
    last_name  = db.Column(db.String(50), nullable=False, default = '')
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    isVerified = db.Column(db.Boolean, nullable=False, default=False)
