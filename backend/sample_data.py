from app import app, db
from components.extensions import datastore, bcrypt
#from components.models import db
#from fake_data import generate_sample_data

with app.app_context():
    db.drop_all()
    db.create_all()
    # Creating Roles
    datastore.find_or_create_role(name="Admin", description="Admins have control over everything")
    datastore.find_or_create_role(name="Instructor", description="Instructors can create and manage projects")
    datastore.find_or_create_role(name="Student", description="Students can apply for projects")
    db.session.commit()
    # Create a User for each role
    if not datastore.find_user(email="admin@gmail.com"):
        datastore.create_user(username="Admin", email="admin@gmail.com", password=bcrypt.generate_password_hash("Admin@12"), roles=["Admin"])
        datastore.create_user(username="Instructor", email="instructor@gmail.com", password=bcrypt.generate_password_hash("Instructor@12"), roles=["Instructor"])
        datastore.create_user(username="Student", email="student@gmail.com", password=bcrypt.generate_password_hash("Student@12"), roles=["Student"])
    
    
    db.session.commit()
