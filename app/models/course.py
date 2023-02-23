from app.extensions import db

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, default = '')
    family = db.Column(db.String(10), nullable=False, default = '')
    number = db.Column(db.String(10), nullable=False, default = '')

    def __repr__(self):
        return f"<Course {self.id}, {self.name}>"
