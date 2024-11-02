from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from flask_security import roles_required
from datetime import datetime, timedelta
from sqlalchemy import and_, or_, desc
from ..models.models import (
    db, Milestone, Project, MilestoneSubmission, Student,
    ProjectStudentAssignment
)
from ..utils.helpers import generate_response, handle_error, instructor_required
import json

milestone_bp = Blueprint('milestones', __name__)

@milestone_bp.route('/', methods=['GET'])
@login_required
def get_milestones():
    """Get list of milestones with filtering options"""
    try:
        # Get query parameters
        project_id = request.args.get('project_id')
        status = request.args.get('status')
        search = request.args.get('search')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        if not project_id:
            return generate_response(message='Project ID is required', status=400)

        # Verify project access
        project = Project.query.get_or_404(project_id)
        if current_user.has_role('student'):
            assignment = ProjectStudentAssignment.query.filter_by(
                project_id=project_id,
                student_id=current_user.user_id
            ).first()
            if not assignment:
                return generate_response(message='Access denied', status=403)

        # Base query
        query = Milestone.query.filter_by(project_id=project_id)

        # Apply filters
        if status:
            query = query.filter(Milestone.status == status)
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Milestone.title.ilike(search_term),
                    Milestone.description.ilike(search_term)
                )
            )

        # Order by deadline
        query = query.order_by(Milestone.deadline)

        # Pagination
        paginated_milestones = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        milestones_data = []
        for milestone in paginated_milestones.items:
            # Get submission statistics
            submissions = MilestoneSubmission.query.filter_by(
                milestone_id=milestone.milestone_id
            ).all()
            
            total_students = ProjectStudentAssignment.query.filter_by(
                project_id=project_id
            ).count()

            milestones_data.append({
                'milestone_id': milestone.milestone_id,
                'title': milestone.title,
                'description': milestone.description,
                'start_date': milestone.start_date.isoformat(),
                'deadline': milestone.deadline.isoformat(),
                'status': milestone.status,
                'weightage': milestone.weightage,
                'is_ai_generated': milestone.is_ai_generated,
                'submission_stats': {
                    'total_submissions': len(submissions),
                    'total_students': total_students,
                    'submission_rate': (len(submissions) / total_students * 100) if total_students > 0 else 0
                }
            })

        return generate_response(data={
            'milestones': milestones_data,
            'total': paginated_milestones.total,
            'pages': paginated_milestones.pages,
            'current_page': page
        })
    except Exception as e:
        return handle_error(e)

@milestone_bp.route('/<string:milestone_id>', methods=['GET'])
@login_required
def get_milestone(milestone_id):
    """Get detailed information about a specific milestone"""
    try:
        milestone = Milestone.query.get_or_404(milestone_id)
        
        # Verify access
        if current_user.has_role('student'):
            assignment = ProjectStudentAssignment.query.filter_by(
                project_id=milestone.project_id,
                student_id=current_user.user_id
            ).first()
            if not assignment:
                return generate_response(message='Access denied', status=403)

        # Get submissions
        submissions = MilestoneSubmission.query\
            .filter_by(milestone_id=milestone_id)\
            .all()

        submissions_data = []
        for submission in submissions:
            student = Student.query.get(submission.student_id)
            submissions_data.append({
                'submission_id': submission.submission_id,
                'student': {
                    'id': student.student_id,
                    'name': student.user.username,
                    'email': student.user.email
                },
                'submission_date': submission.submission_date.isoformat(),
                'status': submission.submission_status,
                'document_path': submission.document_path,
                'ai_analysis': {
                    'status': submission.ai_analysis_status,
                    'result': json.loads(submission.ai_analysis_result) if submission.ai_analysis_result else None
                }
            })

        return generate_response(data={
            'milestone_details': {
                'milestone_id': milestone.milestone_id,
                'title': milestone.title,
                'description': milestone.description,
                'project_id': milestone.project_id,
                'start_date': milestone.start_date.isoformat(),
                'deadline': milestone.deadline.isoformat(),
                'status': milestone.status,
                'weightage': milestone.weightage,
                'is_ai_generated': milestone.is_ai_generated,
                'created_at': milestone.created_at.isoformat(),
                'created_by': {
                    'instructor_id': milestone.created_by,
                    'name': milestone.instructor.user.username
                }
            },
            'submissions': submissions_data
        })
    except Exception as e:
        return handle_error(e)

@milestone_bp.route('/', methods=['POST'])
@login_required
@instructor_required
def create_milestone():
    """Create a new milestone"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'description', 'project_id', 'start_date', 
                         'deadline', 'weightage']
        for field in required_fields:
            if field not in data:
                return generate_response(
                    message=f'Missing required field: {field}',
                    status=400
                )

        # Verify project and instructor permission
        project = Project.query.get_or_404(data['project_id'])
        if project.instructor_id != current_user.instructor.instructor_id:
            return generate_response(message='Unauthorized access', status=403)

        # Create milestone
        milestone = Milestone(
            title=data['title'],
            description=data['description'],
            project_id=data['project_id'],
            start_date=datetime.fromisoformat(data['start_date']),
            deadline=datetime.fromisoformat(data['deadline']),
            weightage=data['weightage'],
            status='pending',
            created_by=current_user.instructor.instructor_id,
            is_ai_generated=False
        )
        db.session.add(milestone)
        db.session.commit()

        return generate_response(
            data={'milestone_id': milestone.milestone_id},
            message='Milestone created successfully',
            status=201
        )
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@milestone_bp.route('/generate', methods=['POST'])
@login_required
@instructor_required
def generate_milestones():
    """Generate milestones using AI"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['project_id', 'project_description', 'duration_weeks']
        for field in required_fields:
            if field not in data:
                return generate_response(
                    message=f'Missing required field: {field}',
                    status=400
                )

        # Verify project and instructor permission
        project = Project.query.get_or_404(data['project_id'])
        if project.instructor_id != current_user.instructor.instructor_id:
            return generate_response(message='Unauthorized access', status=403)

        # TODO: Implement AI milestone generation logic here
        # For now, create sample milestones
        milestones = []
        start_date = project.start_date
        weeks_per_milestone = int(data['duration_weeks']) // 5  # 5 milestones

        for i in range(5):
            milestone = Milestone(
                title=f"Milestone {i+1}",
                description=f"Auto-generated milestone {i+1}",
                project_id=data['project_id'],
                start_date=start_date,
                deadline=start_date + timedelta(weeks=weeks_per_milestone),
                weightage=20.0,  # Equal weightage
                status='pending',
                created_by=current_user.instructor.instructor_id,
                is_ai_generated=True
            )
            milestones.append(milestone)
            start_date += timedelta(weeks=weeks_per_milestone)

        db.session.bulk_save_objects(milestones)
        db.session.commit()

        return generate_response(
            data={'milestone_count': len(milestones)},
            message='Milestones generated successfully'
        )
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@milestone_bp.route('/<string:milestone_id>', methods=['PUT'])
@login_required
@instructor_required
def update_milestone(milestone_id):
    """Update milestone information"""
    try:
        milestone = Milestone.query.get_or_404(milestone_id)
        
        # Verify instructor permission
        project = Project.query.get(milestone.project_id)
        if project.instructor_id != current_user.instructor.instructor_id:
            return generate_response(message='Unauthorized access', status=403)

        data = request.get_json()

        # Update fields
        if 'title' in data:
            milestone.title = data['title']
        if 'description' in data:
            milestone.description = data['description']
        if 'start_date' in data:
            milestone.start_date = datetime.fromisoformat(data['start_date'])
        if 'deadline' in data:
            milestone.deadline = datetime.fromisoformat(data['deadline'])
        if 'weightage' in data:
            milestone.weightage = data['weightage']
        if 'status' in data:
            milestone.status = data['status']

        db.session.commit()
        return generate_response(message='Milestone updated successfully')
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@milestone_bp.route('/<string:milestone_id>/submissions', methods=['POST'])
@login_required
def submit_milestone(milestone_id):
    """Submit work for a milestone"""
    try:
        milestone = Milestone.query.get_or_404(milestone_id)
        
        # Verify student is assigned to project
        assignment = ProjectStudentAssignment.query.filter_by(
            project_id=milestone.project_id,
            student_id=current_user.user_id
        ).first()
        if not assignment:
            return generate_response(message='Not assigned to this project', status=403)

        # Handle file upload
        if 'file' not in request.files:
            return generate_response(message='No file provided', status=400)
        
        file = request.files['file']
        if file.filename == '':
            return generate_response(message='No file selected', status=400)

        # Save file logic would go here
        # For now, just store the filename
        submission = MilestoneSubmission(
            milestone_id=milestone_id,
            student_id=current_user.user_id,
            document_path=file.filename,
            submission_status='submitted',
            ai_analysis_status='pending'
        )
        db.session.add(submission)
        db.session.commit()

        return generate_response(
            data={'submission_id': submission.submission_id},
            message='Submission successful'
        )
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@milestone_bp.route('/<string:milestone_id>/status', methods=['GET'])
@login_required
def get_milestone_status(milestone_id):
    """Get milestone completion status for all students"""
    try:
        milestone = Milestone.query.get_or_404(milestone_id)
        
        # Get all students assigned to the project
        students = Student.query\
            .join(ProjectStudentAssignment)\
            .filter(ProjectStudentAssignment.project_id == milestone.project_id)\
            .all()

        status_data = []
        for student in students:
            submission = MilestoneSubmission.query.filter_by(
                milestone_id=milestone_id,
                student_id=student.student_id
            ).first()

            status_data.append({
                'student_id': student.student_id,
                'name': student.user.username,
                'email': student.user.email,
                'submission_status': submission.submission_status if submission else 'pending',
                'submission_date': submission.submission_date.isoformat() if submission else None,
                'ai_analysis_status': submission.ai_analysis_status if submission else None
            })

        return generate_response(data={
            'milestone_status': milestone.status,
            'deadline': milestone.deadline.isoformat(),
            'student_submissions': status_data
        })
    except Exception as e:
        return handle_error(e)

# Error handlers
@milestone_bp.errorhandler(404)
def not_found_error(error):
    return generate_response(message='Milestone not found', status=404)

@milestone_bp.errorhandler(403)
def forbidden_error(error):
    return generate_response(message='Forbidden', status=403)
