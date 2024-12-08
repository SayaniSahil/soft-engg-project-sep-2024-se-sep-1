from flask import Blueprint, request, jsonify
from flask_security import auth_required, roles_required, current_user
from datetime import datetime, timedelta
from components.extensions import db
from components.models import Milestone, Project, MilestoneSubmission, User, ProjectInstructorAssignment, ProjectStudentAssignment
from utils.helpers import handle_error
import json

milestone_bp = Blueprint('milestones', __name__)

@milestone_bp.route('/instructor/milestones/<int:instructor_id>', methods=['GET'])
@auth_required('token')
def get_instructor_milestones(instructor_id: int):
    """Get all milestones for a specific project."""

    # Verify project exists
    project = ProjectInstructorAssignment.query.filter_by(instructor_id=instructor_id).first()
    if not project: return jsonify({"error": "Project not found"}), 404
    project_id = project.project_id

    # Get milestones
    milestones = Milestone.query.filter_by(project_id=project_id).order_by(Milestone.start_date).all()

    response_data = [{
        'id': milestone.milestone_id,
        'title': milestone.title,
        'description': milestone.description,
        'start_date': milestone.start_date.isoformat(),
        'end_date': milestone.end_date.isoformat(),
        'weightage': milestone.weightage,
        'document_url': milestone.document_url,
    } for milestone in milestones]

    return jsonify({"message": "Milestones retrieved successfully", "milestones": response_data}), 200

@milestone_bp.route('/student/milestones/<int:student_id>', methods=['GET'])
@auth_required('token')
def get_student_milestones(student_id):
    # Verify project exists
    project = ProjectStudentAssignment.query.filter_by(student_id=student_id).first()
    if not project: return jsonify({"message": "Project not found"}), 404
    
    project_id = project.project_id

    # Get all milestones for the project
    milestones = Milestone.query.filter_by(project_id=project_id).order_by(Milestone.start_date).all()

    response_data = []
    for milestone in milestones:
        # Get student's submission for this milestone
        submission = MilestoneSubmission.query.filter_by(
            milestone_id=milestone.milestone_id,
            student_id=student_id
        ).first()

        milestone_data = {
            'id': milestone.milestone_id,
            'title': milestone.title,
            'description': milestone.description,
            'status': 'pending' if not submission else 'completed',
            'weightage': milestone.weightage,
            'end_date': milestone.end_date.isoformat(),
            'document_url': milestone.document_url
        }
        response_data.append(milestone_data)

    return jsonify({"message": "Milestones retrieved successfully", "milestones": response_data}), 200

@milestone_bp.route('/instructor/milestones/<int:milestone_id>', methods=['PUT'])
@auth_required('token')
def update_milestone(milestone_id: int):
    milestone = Milestone.query.get(milestone_id)
    if not milestone: return jsonify({'message': 'Milestone not found'}), 404

    data = request.get_json()
    
    # Validate required fields
    required_fields = ['title', 'description', 'start_date', 'end_date']
    flag = True
    for field in required_fields:
        if field in data: 
            flag = False
            break
    if flag: return jsonify({'message': 'At least one field is required'}), 400

    # Validate dates
    start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date() if 'start_date' in data else milestone.start_date
    end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date() if 'end_date' in data else milestone.end_date
    
    if end_date < start_date:
        return jsonify({'message': 'End date cannot be before start date'}), 400

    # Update milestone fields
    milestone.title = data['title'] if 'title' in data else milestone.title
    milestone.description = data['description'] if 'description' in data else milestone.description
    milestone.start_date = start_date if 'start_date' in data else milestone.start_date
    milestone.end_date = end_date if 'end_date' in data else milestone.end_date
    milestone.weightage = data.get('weightage', milestone.weightage)
    
    if 'document_url' in data:
        milestone.document_url = data['document_url']

    # Update the milestone in database
    db.session.commit()
    
    # Prepare response data
    response_data = {
        'id': milestone.milestone_id,
        'title': milestone.title,
        'description': milestone.description,
        'start_date': milestone.start_date.isoformat(),
        'end_date': milestone.end_date.isoformat(),
        'weightage': milestone.weightage,
        'document_url': milestone.document_url
    }

    return jsonify({'message': 'Milestone updated successfully','milestone': response_data}), 200

@milestone_bp.route('/instructor/milestones/<milestone_id>', methods=['DELETE'])
@auth_required('token')

def delete_milestone(milestone_id):
    """Delete a milestone."""
    try:
        milestone = Milestone.query.get(milestone_id)
        if not milestone:
            return jsonify({
                'status': 'error',
                'message': 'Milestone not found'
            }), 404
            
        db.session.delete(milestone)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Milestone deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return handle_error(e)