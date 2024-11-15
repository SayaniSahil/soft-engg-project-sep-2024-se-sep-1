from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from datetime import datetime
from sqlalchemy.orm import relationship, backref
from sqlalchemy import DateTime

db = SQLAlchemy()

# Flask-Security-Too association tables
roles_users = db.Table('roles_users',
    db.Column('user_id', db.String(20), db.ForeignKey('users.user_id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    user_id = db.Column(db.String(20), primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False) # Session ID
    
    roles = relationship('Role', secondary=roles_users,
                        backref=backref('users', lazy='dynamic'))
    

class Student(db.Model):
    __tablename__ = 'students'
    
    student_id = db.Column(db.String(20), primary_key=True)
    user_id = db.Column(db.String(20), db.ForeignKey('users.user_id'), nullable=False)
    department = db.Column(db.String(100))
    batch = db.Column(db.String(20))
    
    user = relationship('User', backref=backref('student', uselist=False))


class Project(db.Model):
    __tablename__ = 'projects'
    
    project_id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    created_at = db.Column(DateTime, default=datetime.utcnow)

class ProjectStudentAssignment(db.Model):
    __tablename__ = 'project_student_assignment'
    
    project_id = db.Column(db.String(20), db.ForeignKey('projects.project_id'), primary_key=True)
    student_id = db.Column(db.String(20), db.ForeignKey('students.student_id'), primary_key=True)
    github_url = db.Column(db.String(255))
    assigned_date = db.Column(DateTime, default=datetime.utcnow)

class ProjectInstructorAssignment(db.Model):
    __tablename__ = 'project_instructor_assignment'
    
    project_id = db.Column(db.String(20), db.ForeignKey('projects.project_id'), primary_key=True)
    instructor_id = db.Column(db.String(20), db.ForeignKey('instructors.instructor_id'), primary_key=True)
    assigned_date = db.Column(DateTime, default=datetime.utcnow)

class Milestone(db.Model):
    __tablename__ = 'milestones'
    
    milestone_id = db.Column(db.String(20), primary_key=True)
    project_id = db.Column(db.String(20), db.ForeignKey('projects.project_id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    weightage = db.Column(db.Float)
    created_at = db.Column(DateTime, default=datetime.utcnow)

class MilestoneSubmission(db.Model):
    __tablename__ = 'milestone_submissions'
    
    submission_id = db.Column(db.String(20), primary_key=True)
    milestone_id = db.Column(db.String(20), db.ForeignKey('milestones.milestone_id'), nullable=False)
    student_id = db.Column(db.String(20), db.ForeignKey('students.student_id'), nullable=False)
    submission_date = db.Column(DateTime, default=datetime.utcnow)
    evaluation_status = db.Column(db.String(20), default='pending')
    evaluation_date = db.Column(DateTime)
    document_url = db.Column(db.String(255))
    
class ChatHistory(db.Model):
    __tablename__ = 'chat_history'
    
    chat_id = db.Column(db.String(20), primary_key=True)
    project_id = db.Column(db.String(20), db.ForeignKey('projects.project_id'), nullable=False)
    instructor_id = db.Column(db.String(20), db.ForeignKey('users.user_id'), nullable=False)
    message_text = db.Column(db.Text, nullable=False)
    message_timestamp = db.Column(DateTime, default=datetime.utcnow)
