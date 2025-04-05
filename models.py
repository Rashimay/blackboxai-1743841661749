from app import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, instructor, student
    year = db.Column(db.Integer)  # Only for students (1-4)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}')"

class Lecture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    qr_code = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f"Lecture('{self.title}', '{self.date}')"

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    proof_image = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f"Attendance('{self.student_id}', '{self.lecture_id}', '{self.timestamp}')"