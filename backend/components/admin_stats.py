from flask import Blueprint, jsonify, request
from sqlalchemy import func
from components.extensions import db
from components.models import (
    Project, ProjectStudentAssignment, Milestone, MilestoneSubmission
)
from datetime import datetime, timedelta

admin_dashboard_bp = Blueprint('admin_dashboard', __name__)

@admin_dashboard_bp.route('/admin/dashboard/statistics', methods=['GET'])
def get_admin_dashboard_statistics():
    """Get statistics for admin dashboard."""
    try:
        # Calculate key statistics
        total_projects = Project.query.count()
        total_students = db.session.query(ProjectStudentAssignment.student_id).distinct().count()

        total_milestones = Milestone.query.count()
        completed_milestones = MilestoneSubmission.query.filter(
            MilestoneSubmission.evaluation_status == 'approved'
        ).count()
        completion_rate = (completed_milestones / total_milestones * 100) if total_milestones > 0 else 0

        active_students = db.session.query(MilestoneSubmission.student_id).distinct().filter(
            MilestoneSubmission.submission_date >= datetime.now() - timedelta(days=7)
        ).count()

        # Prepare the response data
        statistics = {
            "total_projects": total_projects,
            "total_students": total_students,
            "active_students": active_students,
            "completion_rate": round(completion_rate, 2)
        }

        return jsonify({"success": True, "data": statistics})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@admin_dashboard_bp.route('/admin/dashboard/projects', methods=['GET'])
def get_all_projects():
    """Fetch all projects with brief details."""
    try:
        projects = Project.query.all()
        project_list = [
            {
                "id": project.project_id,
                "title": project.title,
                "description": project.description,
                "created_at": project.created_at.strftime('%Y-%m-%d')
            } for project in projects
        ]
        return jsonify({"success": True, "data": {"projects": project_list}})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@admin_dashboard_bp.route('/admin/dashboard/students', methods=['GET'])
def get_all_students():
    """Fetch all students assigned to projects."""
    try:
        student_assignments = ProjectStudentAssignment.query.all()
        student_list = [
            {
                "student_id": assignment.student_id,
                "project_id": assignment.project_id,
                "assigned_date": assignment.assigned_date.strftime('%Y-%m-%d')
            } for assignment in student_assignments
        ]
        return jsonify({"success": True, "data": {"students": student_list}})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@admin_dashboard_bp.route('/admin/dashboard/milestones', methods=['GET'])
def get_milestone_details():
    """Fetch milestone details and their completion status."""
    try:
        milestones = Milestone.query.all()
        milestone_list = [
            {
                "id": milestone.milestone_id,
                "title": milestone.title,
                "status": "Completed" if MilestoneSubmission.query.filter_by(
                    milestone_id=milestone.milestone_id, evaluation_status='approved'
                ).count() > 0 else "Pending"
            } for milestone in milestones
        ]
        return jsonify({"success": True, "data": {"milestones": milestone_list}})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@admin_dashboard_bp.route('/admin/dashboard/milestone_submissions', methods=['POST'])
def filter_milestone_submissions():
    """Filter milestone submissions by student or project."""
    try:
        data = request.json
        student_id = data.get('student_id')
        project_id = data.get('project_id')

        query = MilestoneSubmission.query

        if student_id:
            query = query.filter_by(student_id=student_id)

        if project_id:
            # Join MilestoneSubmission with Milestone and filter by project_id
            query = query.join(Milestone).filter(Milestone.project_id == project_id)

        submissions = query.all()
        submission_list = [
            {
                "id": submission.submission_id,
                "milestone_id": submission.milestone_id,
                "student_id": submission.student_id,
                "submission_date": submission.submission_date.strftime('%Y-%m-%d'),
                "evaluation_status": submission.evaluation_status
            } for submission in submissions
        ]
        return jsonify({"success": True, "data": {"submissions": submission_list}})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
