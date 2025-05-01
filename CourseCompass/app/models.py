from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    grades = db.relationship('Grade', backref='user', lazy=True)

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.Float, nullable=False)  # This is the percentage (e.g., 88.5)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

