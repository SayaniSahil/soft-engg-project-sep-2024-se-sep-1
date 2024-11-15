from flask import Blueprint, request, jsonify
from flask_security import roles_required, current_user
import pandas as pd
from io import StringIO
from models import db, Student, User
from werkzeug.security import generate_password_hash
import uuid

student_bp = Blueprint('student', __name__)

# BULK UPLOAD FORMAT
# student_id,email,username,password,department,batch
# S001,student1@example.com,student1,password123,Computer Science,2024
# S002,student2@example.com,student2,password123,Electrical,2024

@student_bp.route('/students/bulk-upload', methods=['POST'])
@roles_required('admin', 'instructor')  # Only admin and instructor can access
def bulk_upload_students():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
            
        # Read CSV file
        csv_data = pd.read_csv(StringIO(file.stream.read().decode("UTF8")))
        
        for _, row in csv_data.iterrows():
            # Check if student already exists
            existing_student = Student.query.filter_by(student_id=row['student_id']).first()
            
            if existing_student:
                # Update existing student
                existing_student.department = row['department']
                existing_student.batch = row['batch']
                
                # Update associated user if email or username provided
                if 'email' in row and row['email']:
                    existing_student.user.email = row['email']
                if 'username' in row and row['username']:
                    existing_student.user.username = row['username']
            else:
                # Create new user
                new_user = User(
                    user_id=str(uuid.uuid4())[:20],
                    email=row['email'],
                    username=row['username'],
                    password=generate_password_hash(row['password']),
                    active=True,
                    fs_uniquifier=str(uuid.uuid4())
                )
                db.session.add(new_user)
                
                # Create new student
                new_student = Student(
                    student_id=row['student_id'],
                    user_id=new_user.user_id,
                    department=row['department'],
                    batch=row['batch']
                )
                db.session.add(new_student)
                
        db.session.commit()
        return jsonify({'message': 'Students uploaded successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@student_bp.route('/students/<student_id>', methods=['DELETE'])
@roles_required('admin', 'instructor')  # Only admin and instructor can access
def delete_student(student_id):
    try:
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
            
        # Delete associated user
        user = User.query.get(student.user_id)
        if user:
            db.session.delete(user)
            
        db.session.delete(student)
        db.session.commit()
        
        return jsonify({'message': 'Student deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500