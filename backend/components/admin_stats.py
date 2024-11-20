# components/statistics/admin_routes.py

from flask import Blueprint
from flask_security import auth_required, roles_required
from sqlalchemy import func
from components.extensions import db, cache
from components.models import (
    Project, ProjectStudentAssignment, ProjectInstructorAssignment,
    Milestone, MilestoneSubmission
)
from utils.helpers import APIResponse
from datetime import datetime, timedelta

admin_stats_bp = Blueprint('admin_statistics', _name_)

@admin_stats_bp.route('/admin/dashboard/statistics', methods=['GET'])
@auth_required('token')
@roles_required('admin')
def get_admin_dashboard_statistics():
    """Get statistics for admin dashboard."""
    try:
        # Check cache
        cache_key = 'admin_dashboard_statistics'
        cached_stats = cache.get(cache_key)
        if cached_stats:
            return APIResponse.success(data=cached_stats)

        # Get main statistics
        total_projects = Project.query.count()
        total_students = db.session.query(
            func.count(distinct(ProjectStudentAssignment.student_id))
        ).scalar() or 0
        
        # Calculate completion rate across all projects
        total_milestones = Milestone.query.count()
        completed_milestones = db.session.query(
            func.count(distinct(MilestoneSubmission.milestone_id))
        ).filter(
            MilestoneSubmission.evaluation_status == 'approved'
        ).scalar() or 0
        
        completion_rate = (completed_milestones / total_milestones * 100) if total_milestones > 0 else 0

        # Get active students (with submissions in last 7 days)
        active_students = db.session.query(
            func.count(distinct(MilestoneSubmission.student_id))
        ).filter(
            MilestoneSubmission.submission_date >= datetime.now() - timedelta(days=7)
        ).scalar() or 0

        # Project statistics with student counts
        projects = Project.query.all()
        project_stats = []
        
        for project in projects:
            student_count = ProjectStudentAssignment.query.filter_by(
                project_id=project.project_id
            ).count()
            
            instructor_count = ProjectInstructorAssignment.query.filter_by(
                project_id=project.project_id
            ).count()
            
            # Get project completion percentage
            project_milestones = Milestone.query.filter_by(
                project_id=project.project_id
            ).count()
            
            completed_count = db.session.query(
                func.count(distinct(MilestoneSubmission.milestone_id))
            ).join(Milestone).filter(
                Milestone.project_id == project.project_id,
                MilestoneSubmission.evaluation_status == 'approved'
            ).scalar() or 0
            
            completion_percentage = (completed_count / project_milestones * 100) if project_milestones > 0 else 0
            
            project_stats.append({
                'project_id': project.project_id,
                'title': project.title,
                'students': student_count,
                'instructors': instructor_count,
                'completion_percentage': round(completion_percentage, 2)
            })

        statistics = {
            "overview_stats": {
                "total_projects": total_projects,
                "active_students": active_students,
                "total_students": total_students,
                "completion_rate": round(completion_rate, 2)
            },
            "projects": project_stats
        }

        # Cache for 5 minutes
        cache.set(cache_key, statistics, timeout=300)
        
        return APIResponse.success(data=statistics)
        
    except Exception as e:
        current_app.logger.error(f"Error fetching admin dashboard statistics: {str(e)}")
        return APIResponse.error(str(e))

@admin_stats_bp.route('/admin/dashboard/project-stats/<int:project_id>', methods=['GET'])
@auth_required('token')
@roles_required('admin')
def get_project_specific_stats(project_id):
    """Get detailed statistics for a specific project."""
    try:
        project = Project.query.get(project_id)
        if not project:
            return APIResponse.error("Project not found", 404)

        # Get project-specific statistics
        student_count = ProjectStudentAssignment.query.filter_by(
            project_id=project_id
        ).count()
        
        # Get milestone statistics
        milestones = Milestone.query.filter_by(project_id=project_id).all()
        milestone_stats = []
        
        for milestone in milestones:
            submissions = MilestoneSubmission.query.filter_by(
                milestone_id=milestone.milestone_id
            ).all()
            
            approved = sum(1 for s in submissions if s.evaluation_status == 'approved')
            pending = sum(1 for s in submissions if s.evaluation_status == 'pending')
            
            milestone_stats.append({
                'title': milestone.title,
                'total_submissions': len(submissions),
                'approved': approved,
                'pending': pending,
                'completion_rate': (approved / student_count * 100) if student_count > 0 else 0
            })

        stats = {
            'project_details': {
                'title': project.title,
                'student_count': student_count,
                'instructor_count': ProjectInstructorAssignment.query.filter_by(
                    project_id=project_id
                ).count(),
                'total_milestones': len(milestones)
            },
            'milestone_stats': milestone_stats,
            'recent_activities': get_recent_activities(project_id)
        }

        return APIResponse.success(data=stats)
        
    except Exception as e:
        current_app.logger.error(f"Error fetching project statistics: {str(e)}")
        return APIResponse.error(str(e))

def get_recent_activities(project_id, days=7):
    """Get recent activities for a project."""
    recent_submissions = MilestoneSubmission.query.join(
        Milestone
    ).filter(
        Milestone.project_id == project_id,
        MilestoneSubmission.submission_date >= datetime.now() - timedelta(days=days)
    ).order_by(
        MilestoneSubmission.submission_date.desc()
    ).limit(5).all()

    return [{
        'student_id': submission.student_id,
        'milestone_id': submission.milestone_id,
        'status': submission.evaluation_status,
        'date': submission.submission_date.strftime('%Y-%m-%d %H:%M')
    } for submission in recent_submissions]

# Register blueprint in app.py
# app.register_blueprint(admin_stats_bp, url_prefix='/api')