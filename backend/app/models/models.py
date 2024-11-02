from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from datetime import datetime
from sqlalchemy.orm import relationship, backref
from sqlalchemy import DateTime
from flask_security.utils import hash_password, verify_password

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
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = db.Column(DateTime)
    
    roles = relationship('Role', secondary=roles_users,
                        backref=backref('users', lazy='dynamic'))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if 'password' in kwargs:
            self.password = hash_password(kwargs['password'])

    def verify_password(self, password):
        return verify_password(password, self.password)

class Instructor(db.Model):
    __tablename__ = 'instructors'
    
    instructor_id = db.Column(db.String(20), db.ForeignKey('users.user_id'), primary_key=True)
    department = db.Column(db.String(100))
    designation = db.Column(db.String(100))
    specialization = db.Column(db.String(200))
    
    # Relationships
    projects = relationship('Project', backref='instructor', lazy=True)
    feedbacks = relationship('Feedback', backref='instructor', lazy=True)
    user = relationship('User', backref=backref('instructor', uselist=False))

class Student(db.Model):
    __tablename__ = 'students'
    
    student_id = db.Column(db.String(20), db.ForeignKey('users.user_id'), primary_key=True)
    batch_year = db.Column(db.String(4))
    program = db.Column(db.String(100))
    github_username = db.Column(db.String(100))
    enrollment_status = db.Column(db.String(20), default='active')
    
    # Relationships
    user = relationship('User', backref=backref('student', uselist=False))
    projects = relationship('Project', secondary='project_student_assignment',
                          backref=backref('students', lazy='dynamic'))

class Project(db.Model):
    __tablename__ = 'projects'
    
    project_id = db.Column(db.String(20), primary_key=True)
    project_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    instructor_id = db.Column(db.String(20), db.ForeignKey('instructors.instructor_id'), nullable=False)
    
    # Cache config for project statistics
    __table_args__ = {
        'info': {'cache_ok': True}
    }

class ProjectStudentAssignment(db.Model):
    __tablename__ = 'project_student_assignment'
    
    project_id = db.Column(db.String(20), db.ForeignKey('projects.project_id'), primary_key=True)
    student_id = db.Column(db.String(20), db.ForeignKey('students.student_id'), primary_key=True)
    assigned_date = db.Column(DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')

class Milestone(db.Model):
    __tablename__ = 'milestones'
    
    milestone_id = db.Column(db.String(20), primary_key=True)
    project_id = db.Column(db.String(20), db.ForeignKey('projects.project_id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date, nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    weightage = db.Column(db.Float)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(20), db.ForeignKey('instructors.instructor_id'), nullable=False)
    is_ai_generated = db.Column(db.Boolean, default=False)

class MilestoneSubmission(db.Model):
    __tablename__ = 'milestone_submissions'
    
    submission_id = db.Column(db.String(20), primary_key=True)
    milestone_id = db.Column(db.String(20), db.ForeignKey('milestones.milestone_id'), nullable=False)
    student_id = db.Column(db.String(20), db.ForeignKey('students.student_id'), nullable=False)
    submission_date = db.Column(DateTime, default=datetime.utcnow)
    document_path = db.Column(db.String(255))
    submission_status = db.Column(db.String(20), nullable=False)
    ai_analysis_status = db.Column(db.String(20), default='pending')
    ai_analysis_result = db.Column(db.Text)

    __table_args__ = (
        db.Index('idx_submission_milestone_student', 'milestone_id', 'student_id'),
    )

class Feedback(db.Model):
    __tablename__ = 'feedback'
    
    feedback_id = db.Column(db.String(20), primary_key=True)
    project_id = db.Column(db.String(20), db.ForeignKey('projects.project_id'), nullable=False)
    milestone_id = db.Column(db.String(20), db.ForeignKey('milestones.milestone_id'))
    student_id = db.Column(db.String(20), db.ForeignKey('students.student_id'), nullable=False)
    instructor_id = db.Column(db.String(20), db.ForeignKey('instructors.instructor_id'), nullable=False)
    feedback_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float)
    marks = db.Column(db.Float)
    feedback_date = db.Column(DateTime, default=datetime.utcnow)
    is_ai_assisted = db.Column(db.Boolean, default=False)

class GithubIntegration(db.Model):
    __tablename__ = 'github_integration'
    
    integration_id = db.Column(db.String(20), primary_key=True)
    student_id = db.Column(db.String(20), db.ForeignKey('students.student_id'), nullable=False)
    project_id = db.Column(db.String(20), db.ForeignKey('projects.project_id'), nullable=False)
    repository_url = db.Column(db.String(255), nullable=False)
    repository_name = db.Column(db.String(100), nullable=False)
    last_commit_hash = db.Column(db.String(40))
    last_sync_timestamp = db.Column(DateTime)
    webhook_enabled = db.Column(db.Boolean, default=False)

    __table_args__ = (
        db.UniqueConstraint('student_id', 'project_id', name='uq_github_integration'),
    )

class GithubCommit(db.Model):
    __tablename__ = 'github_commits'
    
    commit_id = db.Column(db.String(40), primary_key=True)
    integration_id = db.Column(db.String(20), db.ForeignKey('github_integration.integration_id'), nullable=False)
    commit_message = db.Column(db.Text)
    commit_timestamp = db.Column(DateTime, nullable=False)
    commit_url = db.Column(db.String(255))
    files_changed = db.Column(db.Integer)
    insertions = db.Column(db.Integer)
    deletions = db.Column(db.Integer)

class ChatHistory(db.Model):
    __tablename__ = 'chat_history'
    
    chat_id = db.Column(db.String(20), primary_key=True)
    project_id = db.Column(db.String(20), db.ForeignKey('projects.project_id'), nullable=False)
    sender_id = db.Column(db.String(20), db.ForeignKey('users.user_id'), nullable=False)
    receiver_id = db.Column(db.String(20), db.ForeignKey('users.user_id'), nullable=False)
    message_text = db.Column(db.Text, nullable=False)
    message_timestamp = db.Column(DateTime, default=datetime.utcnow)
    document_id = db.Column(db.String(20), db.ForeignKey('documents.document_id'))
    is_exported = db.Column(db.Boolean, default=False)

class Document(db.Model):
    __tablename__ = 'documents'
    
    document_id = db.Column(db.String(20), primary_key=True)
    project_id = db.Column(db.String(20), db.ForeignKey('projects.project_id'), nullable=False)
    uploaded_by = db.Column(db.String(20), db.ForeignKey('users.user_id'), nullable=False)
    document_type = db.Column(db.String(20), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    upload_timestamp = db.Column(DateTime, default=datetime.utcnow)
    file_size = db.Column(db.BigInteger)
    mime_type = db.Column(db.String(100))

# Add cache configuration
from flask_caching import Cache
cache = Cache(config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0'
})

# Create indexes for performance
def create_indexes():
    db.session.execute(db.text('''
        CREATE INDEX IF NOT EXISTS idx_user_email ON users(email);
        CREATE INDEX IF NOT EXISTS idx_project_status ON projects(status);
        CREATE INDEX IF NOT EXISTS idx_milestone_deadline ON milestones(deadline);
        CREATE INDEX IF NOT EXISTS idx_submission_date ON milestone_submissions(submission_date);
        CREATE INDEX IF NOT EXISTS idx_commit_timestamp ON github_commits(commit_timestamp);
    '''))
    db.session.commit()