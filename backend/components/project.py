from flask import Blueprint, request, jsonify, abort
from flask_security import auth_required
from datetime import datetime
from components.models import Project, db

# Define a Blueprint for project operations
project_bp = Blueprint('project', __name__)

# Route to create a new project
@project_bp.route('/projects', methods=['POST'])
@auth_required()
def create_project():
    data = request.json
    title = data.get('title')
    description = data.get('description')

    if not title or not description:
        return jsonify({"message": "Title and description are required"}), 400

    new_project = Project(
        title=title,
        description=description,
        created_at=datetime.utcnow()
    )

    db.session.add(new_project)
    db.session.commit()
    return jsonify({"message": "Project created successfully", "project": {
        "project_id": new_project.project_id,
        "title": new_project.title,
        "description": new_project.description,
        "created_at": new_project.created_at
    }}), 201

# Route to read (get) all projects
@project_bp.route('/projects', methods=['GET'])
@auth_required()
def get_projects():
    projects = Project.query.all()
    project_list = [{
        "project_id": project.project_id,
        "title": project.title,
        "description": project.description,
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
def update_project(project_id):
    project = Project.query.get_or_404(project_id)
    data = request.json
    title = data.get('title')
    description = data.get('description')

    if not title and not description:
        return jsonify({"error": "Title and description are required"}), 400

    project.title = title if title else project.title
    project.description = description if description else project.description
    db.session.commit()

    return jsonify({"message": "Project updated successfully", "project": {
        "project_id": project.project_id,
        "title": project.title,
        "description": project.description,
        "created_at": project.created_at
    }}), 200

# Route to delete a project
@project_bp.route('/projects/<int:project_id>', methods=['DELETE'])
@auth_required()
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()

    return jsonify({"message": "Project deleted successfully"}), 200
