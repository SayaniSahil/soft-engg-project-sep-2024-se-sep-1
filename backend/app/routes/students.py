from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from flask_security import roles_required
from datetime import datetime
from sqlalchemy import and_, or_
from ..models.models import (
    db, Student, User, Project, ProjectStudentAssignment,
    MilestoneSubmission, GithubIntegration, GithubCommit
)
from ..utils.helpers import generate_response, handle_error, admin_required, instructor_required

student_bp = Blueprint('students', __name__)

@student_bp.route('/', methods=['GET'])
@login_required
def get_students():
    """Get list of students with filtering options"""
    try:
        # Get query parameters
        term = request.args.get('term')
        status = request.args.get('status')
        program = request.args.get('program')
        search = request.args.get('search')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        # Base query
        query = Student.query.join(User)

        # Apply filters
        if term:
            query = query.filter(Student.enrollment_term == term)
        if status:
            query = query.filter(Student.enrollment_status == status)
        if program:
            query = query.filter(Student.program == program)
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    User.email.ilike(search_term),
                    Student.student_id.ilike(search_term),
                    User.username.ilike(search_term)
                )
            )

        # Pagination
        paginated_students = query.paginate(
            page=page, 
            per_page=per_page,
            error_out=False
        )

        # Prepare response
        students_data = [{
            'student_id': student.student_id,
            'email': student.user.email,
            'username': student.user.username,
            'enrollment_term': student.enrollment_term,
            'program': student.program,
            'github_username': student.github_username,
            'status': student.enrollment_status,
            'created_at': student.user.created_at.isoformat()
        } for student in paginated_students.items]

        return generate_response(data={
            'students': students_data,
            'total': paginated_students.total,
            'pages': paginated_students.pages,
            'current_page': page
        })
    except Exception as e:
        return handle_error(e)

@student_bp.route('/<string:student_id>', methods=['GET'])
@login_required
def get_student(student_id):
    """Get detailed information about a specific student"""
    try:
        student = Student.query.get_or_404(student_id)
        
        # Check permissions
        if not current_user.has_role('admin') and \
           not current_user.has_role('instructor') and \
           current_user.user_id != student_id:
            return generate_response(message='Unauthorized access', status=403)

        # Get project assignments
        projects = Project.query.join(ProjectStudentAssignment)\
            .filter(ProjectStudentAssignment.student_id == student_id)\
            .all()

        # Get GitHub activity if available
        github_activity = None
        github_integration = GithubIntegration.query.filter_by(student_id=student_id).first()
        if github_integration:
            recent_commits = GithubCommit.query\
                .filter_by(integration_id=github_integration.integration_id)\
                .order_by(GithubCommit.commit_timestamp.desc())\
                .limit(5)\
                .all()
            github_activity = {
                'repository_url': github_integration.repository_url,
                'recent_commits': [{
                    'commit_id': commit.commit_id,
                    'message': commit.commit_message,
                    'timestamp': commit.commit_timestamp.isoformat(),
                    'files_changed': commit.files_changed
                } for commit in recent_commits]
            }

        return generate_response(data={
            'student_details': {
                'student_id': student.student_id,
                'email': student.user.email,
                'username': student.user.username,
                'enrollment_term': student.enrollment_term,
                'program': student.program,
                'github_username': student.github_username,
                'status': student.enrollment_status,
                'created_at': student.user.created_at.isoformat()
            },
            'projects': [{
                'project_id': project.project_id,
                'name': project.project_name,
                'status': project.status
            } for project in projects],
            'github_activity': github_activity
        })
    except Exception as e:
        return handle_error(e)

@student_bp.route('/', methods=['POST'])
@login_required
@admin_required
def create_student():
    """Create a new student"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'username', 'password', 'enrollment_term', 'program']
        for field in required_fields:
            if field not in data:
                return generate_response(
                    message=f'Missing required field: {field}',
                    status=400
                )

        # Check if email already exists
        if User.query.filter_by(email=data['email']).first():
            return generate_response(
                message='Email already registered',
                status=400
            )

        # Create user
        user = User(
            email=data['email'],
            username=data['username'],
            active=True
        )
        user.password = data['password']  # This will be hashed by the User model
        db.session.add(user)
        db.session.flush()  # Get user_id without committing

        # Create student
        student = Student(
            student_id=user.user_id,
            enrollment_term=data['enrollment_term'],
            program=data['program'],
            github_username=data.get('github_username'),
            enrollment_status='active'
        )
        db.session.add(student)
        db.session.commit()

        return generate_response(
            data={'student_id': student.student_id},
            message='Student created successfully',
            status=201
        )
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@student_bp.route('/<string:student_id>', methods=['PUT'])
@login_required
@admin_required
def update_student(student_id):
    """Update student information"""
    try:
        student = Student.query.get_or_404(student_id)
        data = request.get_json()

        # Update student fields
        if 'enrollment_term' in data:
            student.enrollment_term = data['enrollment_term']
        if 'program' in data:
            student.program = data['program']
        if 'github_username' in data:
            student.github_username = data['github_username']
        if 'enrollment_status' in data:
            student.enrollment_status = data['enrollment_status']

        # Update user fields
        if 'email' in data:
            student.user.email = data['email']
        if 'username' in data:
            student.user.username = data['username']

        db.session.commit()
        return generate_response(message='Student updated successfully')
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@student_bp.route('/<string:student_id>/progress', methods=['GET'])
@login_required
def get_student_progress(student_id):
    """Get student's progress across all projects and milestones"""
    try:
        # Verify access permissions
        if not current_user.has_role('admin') and \
           not current_user.has_role('instructor') and \
           current_user.user_id != student_id:
            return generate_response(message='Unauthorized access', status=403)

        # Get all project assignments
        assignments = ProjectStudentAssignment.query\
            .filter_by(student_id=student_id)\
            .all()

        projects_progress = []
        overall_completion = 0
        total_projects = len(assignments)

        for assignment in assignments:
            project = assignment.project
            
            # Get milestone submissions for this project
            submissions = MilestoneSubmission.query\
                .join(Project)\
                .filter(
                    and_(
                        MilestoneSubmission.student_id == student_id,
                        Project.project_id == project.project_id
                    )
                ).all()

            # Calculate project completion
            total_milestones = len(project.milestones)
            completed_milestones = sum(1 for s in submissions if s.submission_status == 'submitted')
            project_completion = (completed_milestones / total_milestones * 100) if total_milestones > 0 else 0

            projects_progress.append({
                'project_id': project.project_id,
                'project_name': project.project_name,
                'completion_percentage': project_completion,
                'milestones': {
                    'total': total_milestones,
                    'completed': completed_milestones,
                    'pending': total_milestones - completed_milestones
                },
                'status': project.status
            })

            overall_completion += project_completion

        # Calculate overall completion percentage
        overall_completion = (overall_completion / total_projects) if total_projects > 0 else 0

        # Get recent activity
        recent_submissions = MilestoneSubmission.query\
            .filter_by(student_id=student_id)\
            .order_by(MilestoneSubmission.submission_date.desc())\
            .limit(5)\
            .all()

        return generate_response(data={
            'overall_progress': overall_completion,
            'projects': projects_progress,
            'recent_activity': [{
                'milestone_id': sub.milestone_id,
                'submission_date': sub.submission_date.isoformat(),
                'status': sub.submission_status
            } for sub in recent_submissions]
        })
    except Exception as e:
        return handle_error(e)

@student_bp.route('/statistics', methods=['GET'])
@login_required
@roles_required('instructor')
def get_student_statistics():
    """Get general statistics about students"""
    try:
        total_students = Student.query.count()
        active_students = Student.query.filter_by(enrollment_status='active').count()
        
        # Students by program
        program_stats = db.session.query(
            Student.program,
            db.func.count(Student.student_id)
        ).group_by(Student.program).all()

        # Students by term
        term_stats = db.session.query(
            Student.enrollment_term,
            db.func.count(Student.student_id)
        ).group_by(Student.enrollment_term).all()

        return generate_response(data={
            'total_students': total_students,
            'active_students': active_students,
            'by_program': dict(program_stats),
            'by_term': dict(term_stats)
        })
    except Exception as e:
        return handle_error(e)

# Error handlers
@student_bp.errorhandler(404)
def not_found_error(error):
    return generate_response(message='Student not found', status=404)

@student_bp.errorhandler(403)
def forbidden_error(error):
    return generate_response(message='Forbidden', status=403)