from flask import Blueprint, request, jsonify, abort
from flask_security import auth_required, roles_required
from datetime import datetime
from components.models import Project, db, ProjectInstructorAssignment, ProjectStudentAssignment
from components.extensions import datastore

# Define a Blueprint for project operations
project_bp = Blueprint('project', __name__)

# Route to create a new project
@project_bp.route('/projects', methods=['POST'])
@auth_required()
@roles_required('Admin')
def create_project():
    # Project will have a title, description, and instructors
    # Instructors will be a list of emails, and will be added in a separate table
    data = request.json
    title = data.get('title')
    description = data.get('description')
    instructors = data.get('instructors')

    if not title or not description or not instructors:
        return jsonify({"error": "Title and description are required"}), 400

    new_project = Project(
        title=title,
        description=description,
        created_at=datetime.utcnow()
    )

    db.session.add(new_project)
    
    # Add instructors to the project
    valid_instructors = []
    for email in instructors:
        # Check if email is valid
        instructor = datastore.find_user(email=email)
        if not instructor: continue
        valid_instructors.append(instructor.email)
        # Add instructor to the project
        assignment = ProjectInstructorAssignment(
            project_id=new_project.project_id,
            instructor_id=instructor.user_id,
            assigned_date=datetime.utcnow()
        )
        db.session.add(assignment)
    db.session.commit()
    
    return jsonify({"message": "Project created successfully", "project": {
        "project_id": new_project.project_id,
        "title": new_project.title,
        "description": new_project.description,
        "instructors": valid_instructors,
        "students": 0,
        "created_at": new_project.created_at
    }}), 201

# Route to read (get) all projects
@project_bp.route('/projects', methods=['GET'])
@auth_required()
@roles_required('Admin')
def get_projects():
    projects = Project.query.all()
    # For each project, we need to get all instructor emails
    for project in projects:
        instructors = ProjectInstructorAssignment.query.filter_by(project_id=project.project_id).all()
        instructors = [datastore.find_user(user_id=assignment.instructor_id) for assignment in instructors]
        project.instructors = [instructor.email for instructor in instructors]
        project.students = ProjectStudentAssignment.query.filter_by(project_id=project.project_id).count()
    
    # Convert projects to a list of dictionaries, and return
    project_list = [{
        "project_id": project.project_id,
        "title": project.title,
        "description": project.description,
        "instructors": project.instructors,
        "students": project.students,
        "created_at": project.created_at
    } for project in projects]

    return jsonify({"projects": project_list}), 200

# Route to read (get) a single project by ID
@project_bp.route('/projects/<int:project_id>', methods=['GET'])
@auth_required()
def get_project(project_id):
    project = Project.query.get_or_404(project_id)
    return jsonify({
        "project_id": project.project_id,
        "title": project.title,
        "description": project.description,
        "created_at": project.created_at
    }), 200

# Route to update a project
@project_bp.route('/projects/<int:project_id>', methods=['PUT'])
@auth_required()
@roles_required('Admin')
def update_project(project_id):
    # Project will have a title, description, and instructors
    project = Project.query.filter_by(project_id=project_id).first()
    if not project: return jsonify({"error": "Project not found"}), 404
    data = request.json
    title = data.get('title')
    description = data.get('description')
    instructors = data.get('instructors')

    if not title and not description and not instructors:
        return jsonify({"error": "Title, Description, and Instructors are required"}), 400

    # Update title and description directly
    project.title = title if title else project.title
    project.description = description if description else project.description
    
    # Delete all instructor assignments for the project
    assignments = ProjectInstructorAssignment.query.filter_by(project_id=project_id).all()
    for assignment in assignments:
        db.session.delete(assignment)
    db.session.commit()
    
    valid_instructors = []
    # Update instructors
    for email in instructors:
        # Check if email is valid
        instructor = datastore.find_user(email=email)
        if not instructor: continue
        valid_instructors.append(instructor.email)
        # Check if instructor is already assigned
        assignment = ProjectInstructorAssignment.query.filter_by(project_id=project.project_id, instructor_id=instructor.user_id).first()
        if assignment: continue
        # Add instructor to the project
        assignment = ProjectInstructorAssignment(
            project_id=project.project_id,
            instructor_id=instructor.user_id,
            assigned_date=datetime.utcnow()
        )
        db.session.add(assignment)
    
    db.session.commit()

    return jsonify({"message": "Project updated successfully", "project": {
        "project_id": project.project_id,
        "title": project.title,
        "description": project.description,
        "instructors": valid_instructors,
        "students": ProjectStudentAssignment.query.filter_by(project_id=project.project_id).count(),
        "created_at": project.created_at
    }}), 200

# Route to delete a project
@project_bp.route('/projects/<int:project_id>', methods=['DELETE'])
@auth_required()
@roles_required('Admin')
def delete_project(project_id):
    project = Project.query.filter_by(project_id=project_id).first()
    if not project: return jsonify({"error": "Project not found"}), 404
    db.session.delete(project)
    
    # Delete all instructor assignments for the project
    assignments = ProjectInstructorAssignment.query.filter_by(project_id=project_id).all()
    for assignment in assignments:
        db.session.delete(assignment)
    
    # Delete all student assignments for the project
    assignments = ProjectStudentAssignment.query.filter_by(project_id=project_id).all()
    for assignment in assignments:
        db.session.delete(assignment)
    db.session.commit()

    return jsonify({"message": "Project deleted successfully"}), 200
