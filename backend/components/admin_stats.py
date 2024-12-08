from flask import Blueprint, jsonify, request
from sqlalchemy import func
from components.extensions import db
from components.models import (
    Project, ProjectStudentAssignment, Milestone, MilestoneSubmission
)
from datetime import datetime, timedelta
from sqlalchemy import and_

admin_dashboard_bp = Blueprint('admin_dashboard', __name__)

@admin_dashboard_bp.route('/admin/dashboard/statistics', methods=['GET'])
def get_admin_dashboard_statistics():
    """Get statistics for admin dashboard."""
    try:
        # Calculate key statistics
        total_projects = Project.query.count() # Total projects
        # number of milestones due this week
        milestones_due_this_week = Milestone.query.filter(
            and_(
                Milestone.end_date >= datetime.now(), 
                Milestone.end_date <= datetime.now() + timedelta(days=7))).count()
        # number of milestones completed this week
        milestones_completed_this_week = MilestoneSubmission.query.filter(MilestoneSubmission.submission_date >= datetime.now() - timedelta(days=7)).count()
        # Number of students assigned to projects
        total_students = db.session.query(ProjectStudentAssignment.student_id).distinct().count()

        # Day by day submission over last 7 days
        daily_submissions = db.session.query(
            func.date(MilestoneSubmission.submission_date).label('date'),
            func.count(MilestoneSubmission.submission_id).label('count')
        ).filter(
            MilestoneSubmission.submission_date >= datetime.now() - timedelta(days=7)
        ).group_by('date').all()
        #print("Check", daily_submissions)
        # Mark all dates, 0 if no submission
        date_set = [datetime.strptime(date, '%Y-%m-%d').date() for date, count in daily_submissions]
        #print("Check", date_set)
        for i in range(7):
            date = (datetime.now() - timedelta(days=i)).date()
            #print(type(date), type(date_set[0]))
            if date not in date_set:
                date = date.strftime('%Y-%m-%d')
                daily_submissions.append((date, 0))
        daily_submissions.sort(key=lambda x: x[0])
        #print("Check", daily_submissions)
        
        # Submission made before, after, on deadline
        submissions = MilestoneSubmission.query.all()
        on_time_submissions = 0
        late_submissions = 0
        early_submissions = 0
        for submission in submissions:
            milestone = Milestone.query.get(submission.milestone_id)
            if not milestone: continue
            submission.submission_date = submission.submission_date.date()
            if submission.submission_date <= milestone.end_date:
                on_time_submissions += 1
            else:
                late_submissions += 1
            if submission.submission_date < milestone.start_date:
                early_submissions += 1
        milestone_submission_stats = [on_time_submissions, late_submissions, early_submissions]
        
        # Density of milestone deadlines
        milestones = Milestone.query.all()
        milestone_density = {}
        for milestone in milestones:
            if milestone.end_date in milestone_density:
                milestone_density[milestone.end_date] += 1
            else:
                milestone_density[milestone.end_date] = 1
        # Change date to string
        milestone_density = {date.strftime('%Y-%m-%d'): count for date, count in milestone_density.items()}

        # Prepare the response data
        statistics = {
            "total_projects": total_projects,
            "milestones_due_this_week": milestones_due_this_week,
            "milestones_completed_this_week": milestones_completed_this_week,
            "total_students": total_students,
            "daily_submissions": [{"date": date, "count": count} for date, count in daily_submissions],
            "milestone_submission_stats": milestone_submission_stats,
            "milestone_density": [{"date": date, "count": count} for date, count in milestone_density.items()]
        }

        return jsonify({"success": True, "data": statistics})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500