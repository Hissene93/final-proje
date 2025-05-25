from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')
    
   
    taught_courses = db.relationship('Course', backref='teacher', lazy=True)
    student_profile = db.relationship('Student', backref='user', uselist=False, lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}')"

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer)
    class_level = db.Column(db.String(50))
    contact = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    grades = db.relationship('Grade', backref='student', lazy=True)
    
    def __repr__(self):
        return f"Student('{self.first_name}', '{self.last_name}')"

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    
    grades = db.relationship('Grade', backref='course', lazy=True)
    
    def __repr__(self):
        return f"Course('{self.name}')"

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    grade = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Grade('{self.grade}')"