from flask import Blueprint, request, jsonify
from flask_security import auth_required, roles_accepted
import pandas as pd
from io import StringIO
from components.models import db, ProjectStudentAssignment, MilestoneSubmission, Milestone, ProjectInstructorAssignment
from components.extensions import datastore, bcrypt

student_bp = Blueprint('student', __name__)

# BULK UPLOAD FORMAT
# student_id,email,username,password
# S001,student1@example.com,student1,password123
# S002,student2@example.com,student2,password123

@student_bp.route('/students/bulk-upload/<int:instructor_id>', methods=['POST'])
@auth_required()
@roles_accepted('Admin', 'Instructor')  # Only admin and instructor can access
def bulk_upload_students(instructor_id):
    try:
        project = ProjectInstructorAssignment.query.filter_by(instructor_id=instructor_id).first()
        if not project: return jsonify({'error': 'Project not found'}), 404
        project_id = project.project_id
        if 'document' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
            
        file = request.files['document']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
            
        # Read CSV file
        file_content = file.stream.read().decode("UTF-8").strip()
        #print("File content:\n", repr(file_content))
        csv_data = pd.read_csv(StringIO(file_content), sep="\t")
        for _, row in csv_data.iterrows():
            # Check if student already exists
            existing_student = datastore.find_user(email=row['email'])
            
            if existing_student:
                # Update associated user if email or username provided
                if 'username' in row and row['username']:
                    existing_student.username = row['username']
                if 'password' in row and row['password']:
                    existing_student.password = bcrypt.generate_password_hash(row['password'])
                # Check if student is already assigned to project
                existing_assignment = ProjectStudentAssignment.query.filter_by(project_id=project_id, student_id=existing_student.user_id).first()
                if existing_assignment: continue
                assignment = ProjectStudentAssignment(project_id=project_id, student_id=existing_student.user_id)
                db.session.add(assignment)
                db.session.commit()
            else:
                # Create new user
                new_user = datastore.create_user(email=row['email'], username=row['username'], password=bcrypt.generate_password_hash(row['password']))
                new_user.roles.append(datastore.find_role('Student'))
                db.session.add(new_user)
                db.session.commit()
                assignment = ProjectStudentAssignment(project_id=project_id, student_id=new_user.user_id)
                db.session.add(assignment)
                db.session.commit()
                
        return jsonify({'message': 'Students uploaded successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@student_bp.route('/students/<int:instructor_id>', methods=['GET'])
@roles_accepted('Admin', 'Instructor')  # Only admin and instructor can access
@auth_required()
def get_students(instructor_id):
    project = ProjectInstructorAssignment.query.filter_by(instructor_id=instructor_id).first()
    if not project: return jsonify({'error': 'Project not found'}), 404
    project_id = project.project_id
    students = ProjectStudentAssignment.query.filter_by(project_id=project_id).all()
    if not students: return jsonify({'message': 'Students fetched successfully', 'students':[]}), 200
    students = [datastore.find_user(user_id=student.student_id) for student in students]
    students = [{'id': student.user_id, 'email': student.email, 'name': student.username} for student in students]
    # Get progress of each student
    total_milestones = Milestone.query.filter_by(project_id=project_id).count()
    for student in students:
        student['progress'] = MilestoneSubmission.query.filter_by(student_id=student['id']).count() / total_milestones * 100
    return jsonify({'message': 'Students fetched successfully', 'students': students, 'total_milestones': total_milestones}), 200


@student_bp.route('/students/<int:instructor_id>', methods=['DELETE'])
@roles_accepted('Admin', 'Instructor')  # Only admin and instructor can access
@auth_required()
def delete_student(instructor_id):
    try:
        project = ProjectInstructorAssignment.query.filter_by(instructor_id=instructor_id).first()
        if not project: return jsonify({'error': 'Project not found'}), 404
        project_id = project.project_id
        id = request.json.get('id')
        student = datastore.find_user(user_id=id)
        if not student: return jsonify({'error': 'Student not found'}), 404
        # Check if role is student
        print(student.roles)
        print([role.name for role in student.roles])
        if 'Student' not in [role.name for role in student.roles]: return jsonify({'error': 'User is not a student'}), 403
            
        # Delete associated user
        assignment = ProjectStudentAssignment.query.filter_by(project_id=project_id, student_id=student.user_id).first()
        if not assignment: return jsonify({'error': 'Student not assigned to project'}), 404
        db.session.delete(assignment)
        db.session.commit()
        
        return jsonify({'message': 'Student deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500