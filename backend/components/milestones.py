from flask import Blueprint, request, jsonify
from flask_security import auth_required, roles_required, current_user
from datetime import datetime, timedelta
from components.extensions import db
from components.models import Milestone, Project, MilestoneSubmission, User, ProjectInstructorAssignment, ProjectStudentAssignment
from utils.helpers import handle_error
import json

milestone_bp = Blueprint('milestones', __name__)

@milestone_bp.route('/instructor/milestones/<int:project_id>', methods=['GET'])
@auth_required('token')
@roles_required('instructor')
def get_instructor_milestones(project_id: int):
    """Get all milestones for a specific project."""

    # Verify project exists
    project = Project.query.get(project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404

    # Get milestones
    milestones = Milestone.query.filter_by(project_id=project_id)\
        .order_by(Milestone.start_date).all()

    response_data = [{
        'id': milestone.milestone_id,
        'title': milestone.title,
        'description': milestone.description,
        'start_date': milestone.start_date.isoformat(),
        'end_date': milestone.end_date.isoformat(),
        'weightage': milestone.weightage,
        'document_url': milestone.document_url,
        'submissions_count': len(milestone.submissions)
    } for milestone in milestones]


    return jsonify({"data": response_data}), 200

@milestone_bp.route('/student/milestones/<int:project_id>', methods=['GET'])
@auth_required('token')
def get_student_milestones(project_id: int):

    # Verify project exists
    project = Project.query.get(project_id)
    if not project:
        return jsonify({"message": "Project not found"}), 404

    # Get milestones with student's submissions
    milestones = Milestone.query.filter_by(project_id=project_id)\
        .order_by(Milestone.start_date).all()

    response_data = []
    for milestone in milestones:
        # Get student's submission for this milestone
        submission = MilestoneSubmission.query.filter_by(
            milestone_id=milestone.milestone_id,
            student_id=current_user.user_id
        ).first()

        milestone_data = {
            'id': milestone.milestone_id,
            'title': milestone.title,
            'description': milestone.description,
            'start_date': milestone.start_date.isoformat(),
            'end_date': milestone.end_date.isoformat(),
            'weightage': milestone.weightage,
            'document_url': milestone.document_url,
            'submission': None if not submission else {
                'id': submission.submission_id,
                'status': submission.evaluation_status,
                'submitted_at': submission.submission_date.isoformat(),
                'document_url': submission.document_url,
                'evaluation_date': submission.evaluation_date.isoformat() if submission.evaluation_date else None
            }
        }
        response_data.append(milestone_data)

    return jsonify({"data": response_data}), 200

@milestone_bp.route('/instructor/milestones/generate', methods=['POST'])
@auth_required('token')

def generate_milestones():
    """Generate milestones based on problem statement."""
    try:
        data = request.get_json()
        problem_statement = data.get('problemStatement')
        project_id = data.get('project_id')
        milestone_count = data.get('milestoneCount', 5)
        
        if not problem_statement or not project_id:
            return jsonify({
                'status': 'error',
                'message': 'Problem statement is required'
            }), 400
            
        # For demo, generate simple milestones
        # In production, integrate with actual AI service
        milestones = []
        base_date = datetime.now()
        
        for i in range(milestone_count):
            milestone = {
                'project_id': project_id,
                'title': f'Milestone {i+1}',
                'description': f'Description for Milestone {i+1}',
                'start_date': (base_date + timedelta(days=i*14)).strftime('%Y-%m-%d'),
                'end_date': (base_date + timedelta(days=(i+1)*14)).strftime('%Y-%m-%d'),
                'weightage': 100/milestone_count
            }
            milestones.append(milestone)
        
        db.session.add_all(milestones)
        db.session.commit()
            
        return jsonify({
            'status': 'success',
            'data': milestones
        }), 200
    except Exception as e:
        return handle_error(e)

@milestone_bp.route('/instructor/milestones', methods=['POST'])
@auth_required('token')

def create_milestone():
    """Create a new milestone."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'description', 'start_date', 'end_date', 'project_id']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'status': 'error',
                    'message': f'{field} is required'
                }), 400
        
        # Create new milestone
        new_milestone = Milestone(
            project_id=data['project_id'],
            title=data['title'],
            description=data['description'],
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
            end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date(),
            weightage=data.get('weightage', 0),
            document_url=data.get('document_url', None)
        )
        
        db.session.add(new_milestone)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Milestone created successfully'
        }), 201
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@milestone_bp.route('/instructor/milestones/<int:milestone_id>', methods=['PUT'])
@auth_required('token')
def update_milestone(milestone_id: int):
    milestone = Milestone.query.get(milestone_id)
    if not milestone:
        return jsonify({
            'status': 'error',
            'message': 'Milestone not found'
        }), 404

    data = request.get_json()
    
    # Validate required fields
    required_fields = ['title', 'description', 'start_date', 'end_date']
    flag = True
    for field in required_fields:
        if field in data: 
            flag = False
            break
    if flag:
        return jsonify({
            'status': 'error',
            'message': 'At least one field is required'
        }), 400

    # Validate dates
    start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date() if 'start_date' in data else milestone.start_date
    end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date() if 'end_date' in data else milestone.end_date
    
    if end_date < start_date:
        return jsonify({
            'status': 'error',
            'message': 'End date cannot be before start date'
        }), 400

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
        'document_url': milestone.document_url,
        'project_id': milestone.project_id
    }

    return jsonify({
        'status': 'success',
        'message': 'Milestone updated successfully',
        'data': response_data
    }), 200

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