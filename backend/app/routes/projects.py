from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from flask_security import roles_required
from sqlalchemy import and_, or_, desc
from datetime import datetime, timedelta
from ..models.models import (
    db, Project, Student, Instructor, ProjectStudentAssignment,
    Milestone, MilestoneSubmission, GithubIntegration
)
from ..utils.helpers import generate_response, handle_error, instructor_required

project_bp = Blueprint('projects', __name__)

@project_bp.route('/', methods=['GET'])
@login_required
def get_projects():
    """Get list of projects with filtering options"""
    try:
        # Get query parameters
        status = request.args.get('status')
        instructor_id = request.args.get('instructor_id')
        search = request.args.get('search')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        # Base query
        query = Project.query

        # Apply role-based filters
        if current_user.has_role('student'):
            # Students see only their assigned projects
            query = query.join(ProjectStudentAssignment)\
                        .filter(ProjectStudentAssignment.student_id == current_user.user_id)
        elif current_user.has_role('instructor'):
            # Instructors see their own projects
            query = query.filter(Project.instructor_id == current_user.instructor.instructor_id)
        # Admins see all projects

        # Apply additional filters
        if status:
            query = query.filter(Project.status == status)
        if instructor_id:
            query = query.filter(Project.instructor_id == instructor_id)
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Project.project_name.ilike(search_term),
                    Project.description.ilike(search_term)
                )
            )

        # Order by creation date
        query = query.order_by(desc(Project.created_at))

        # Pagination
        paginated_projects = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        projects_data = []
        for project in paginated_projects.items:
            # Get student count and milestone progress
            student_count = ProjectStudentAssignment.query\
                .filter_by(project_id=project.project_id)\
                .count()
            
            total_milestones = len(project.milestones)
            completed_milestones = sum(
                1 for m in project.milestones if m.status == 'completed'
            )

            projects_data.append({
                'project_id': project.project_id,
                'name': project.project_name,
                'description': project.description,
                'status': project.status,
                'start_date': project.start_date.isoformat(),
                'end_date': project.end_date.isoformat(),
                'instructor': {
                    'id': project.instructor.instructor_id,
                    'name': project.instructor.user.username
                },
                'students_count': student_count,
                'milestones': {
                    'total': total_milestones,
                    'completed': completed_milestones
                },
                'created_at': project.created_at.isoformat()
            })

        return generate_response(data={
            'projects': projects_data,
            'total': paginated_projects.total,
            'pages': paginated_projects.pages,
            'current_page': page
        })
    except Exception as e:
        return handle_error(e)

@project_bp.route('/<string:project_id>', methods=['GET'])
@login_required
def get_project(project_id):
    """Get detailed information about a specific project"""
    try:
        project = Project.query.get_or_404(project_id)

        # Check access permissions
        if current_user.has_role('student'):
            assignment = ProjectStudentAssignment.query.filter_by(
                project_id=project_id,
                student_id=current_user.user_id
            ).first()
            if not assignment:
                return generate_response(message='Access denied', status=403)

        # Get students assigned to the project
        students = Student.query\
            .join(ProjectStudentAssignment)\
            .filter(ProjectStudentAssignment.project_id == project_id)\
            .all()

        # Get milestone details with submission stats
        milestones_data = []
        for milestone in project.milestones:
            submissions_count = MilestoneSubmission.query\
                .filter_by(milestone_id=milestone.milestone_id)\
                .count()
            
            milestones_data.append({
                'milestone_id': milestone.milestone_id,
                'title': milestone.title,
                'description': milestone.description,
                'deadline': milestone.deadline.isoformat(),
                'status': milestone.status,
                'weightage': milestone.weightage,
                'submissions_count': submissions_count
            })

        return generate_response(data={
            'project_details': {
                'project_id': project.project_id,
                'name': project.project_name,
                'description': project.description,
                'status': project.status,
                'start_date': project.start_date.isoformat(),
                'end_date': project.end_date.isoformat(),
                'instructor': {
                    'id': project.instructor.instructor_id,
                    'name': project.instructor.user.username,
                    'email': project.instructor.user.email
                },
                'created_at': project.created_at.isoformat(),
                'updated_at': project.updated_at.isoformat()
            },
            'students': [{
                'student_id': student.student_id,
                'name': student.user.username,
                'email': student.user.email,
                'enrollment_term': student.enrollment_term
            } for student in students],
            'milestones': milestones_data
        })
    except Exception as e:
        return handle_error(e)

@project_bp.route('/', methods=['POST'])
@login_required
@instructor_required
def create_project():
    """Create a new project"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'description', 'start_date', 'end_date']
        for field in required_fields:
            if field not in data:
                return generate_response(
                    message=f'Missing required field: {field}',
                    status=400
                )

        # Create project
        project = Project(
            project_name=data['name'],
            description=data['description'],
            start_date=datetime.fromisoformat(data['start_date']),
            end_date=datetime.fromisoformat(data['end_date']),
            instructor_id=current_user.instructor.instructor_id,
            status='active'
        )
        db.session.add(project)
        
        # Assign students if provided
        if 'student_ids' in data:
            for student_id in data['student_ids']:
                assignment = ProjectStudentAssignment(
                    project_id=project.project_id,
                    student_id=student_id
                )
                db.session.add(assignment)

        db.session.commit()

        return generate_response(
            data={'project_id': project.project_id},
            message='Project created successfully',
            status=201
        )
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@project_bp.route('/<string:project_id>', methods=['PUT'])
@login_required
@instructor_required
def update_project(project_id):
    """Update project information"""
    try:
        project = Project.query.get_or_404(project_id)
        
        # Verify instructor permission
        if project.instructor_id != current_user.instructor.instructor_id:
            return generate_response(message='Unauthorized access', status=403)

        data = request.get_json()

        # Update project fields
        if 'name' in data:
            project.project_name = data['name']
        if 'description' in data:
            project.description = data['description']
        if 'start_date' in data:
            project.start_date = datetime.fromisoformat(data['start_date'])
        if 'end_date' in data:
            project.end_date = datetime.fromisoformat(data['end_date'])
        if 'status' in data:
            project.status = data['status']

        # Update student assignments if provided
        if 'student_ids' in data:
            # Remove existing assignments
            ProjectStudentAssignment.query\
                .filter_by(project_id=project_id)\
                .delete()
            
            # Add new assignments
            for student_id in data['student_ids']:
                assignment = ProjectStudentAssignment(
                    project_id=project_id,
                    student_id=student_id
                )
                db.session.add(assignment)

        db.session.commit()
        return generate_response(message='Project updated successfully')
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@project_bp.route('/<string:project_id>/students', methods=['POST'])
@login_required
@instructor_required
def assign_students(project_id):
    """Assign students to project"""
    try:
        project = Project.query.get_or_404(project_id)
        
        # Verify instructor permission
        if project.instructor_id != current_user.instructor.instructor_id:
            return generate_response(message='Unauthorized access', status=403)

        data = request.get_json()
        if 'student_ids' not in data:
            return generate_response(message='Student IDs required', status=400)

        # Add new assignments
        for student_id in data['student_ids']:
            # Check if assignment already exists
            existing = ProjectStudentAssignment.query.filter_by(
                project_id=project_id,
                student_id=student_id
            ).first()
            
            if not existing:
                assignment = ProjectStudentAssignment(
                    project_id=project_id,
                    student_id=student_id
                )
                db.session.add(assignment)

        db.session.commit()
        return generate_response(message='Students assigned successfully')
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@project_bp.route('/<string:project_id>/students/<string:student_id>', methods=['DELETE'])
@login_required
@instructor_required
def remove_student(project_id, student_id):
    """Remove student from project"""
    try:
        project = Project.query.get_or_404(project_id)
        
        # Verify instructor permission
        if project.instructor_id != current_user.instructor.instructor_id:
            return generate_response(message='Unauthorized access', status=403)

        ProjectStudentAssignment.query\
            .filter_by(project_id=project_id, student_id=student_id)\
            .delete()
        
        db.session.commit()
        return generate_response(message='Student removed from project')
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@project_bp.route('/<string:project_id>/progress', methods=['GET'])
@login_required
def get_project_progress(project_id):
    """Get overall project progress and statistics"""
    try:
        project = Project.query.get_or_404(project_id)
        
        # Check access permissions
        if current_user.has_role('student'):
            assignment = ProjectStudentAssignment.query.filter_by(
                project_id=project_id,
                student_id=current_user.user_id
            ).first()
            if not assignment:
                return generate_response(message='Access denied', status=403)

        # Get milestone statistics
        milestone_stats = {
            'total': 0,
            'completed': 0,
            'in_progress': 0,
            'pending': 0,
            'overdue': 0
        }

        today = datetime.now().date()
        for milestone in project.milestones:
            milestone_stats['total'] += 1
            if milestone.status == 'completed':
                milestone_stats['completed'] += 1
            elif milestone.status == 'in_progress':
                milestone_stats['in_progress'] += 1
            elif milestone.deadline < today:
                milestone_stats['overdue'] += 1
            else:
                milestone_stats['pending'] += 1

        # Get student progress
        student_progress = []
        assignments = ProjectStudentAssignment.query\
            .filter_by(project_id=project_id)\
            .all()

        for assignment in assignments:
            submitted_milestones = MilestoneSubmission.query\
                .join(Milestone)\
                .filter(
                    and_(
                        MilestoneSubmission.student_id == assignment.student_id,
                        Milestone.project_id == project_id
                    )
                ).count()
            
            completion_rate = (submitted_milestones / milestone_stats['total'] * 100) \
                if milestone_stats['total'] > 0 else 0

            student_progress.append({
                'student_id': assignment.student_id,
                'name': assignment.student.user.username,
                'submitted_milestones': submitted_milestones,
                'completion_rate': completion_rate
            })

        return generate_response(data={
            'project_status': project.status,
            'milestone_statistics': milestone_stats,
            'student_progress': student_progress,
            'overall_completion': milestone_stats['completed'] / milestone_stats['total'] * 100 \
                if milestone_stats['total'] > 0 else 0,
            'time_remaining': (project.end_date - today).days
        })
    except Exception as e:
        return handle_error(e)

# Error handlers
@project_bp.errorhandler(404)
def not_found_error(error):
    return generate_response(message='Project not found', status=404)

@project_bp.errorhandler(403)
def forbidden_error(error):
    return generate_response(message='Forbidden', status=403)
