from typing import Dict, List, Any
from sqlalchemy import func
from datetime import datetime
from components.models import (
    Project, Milestone, MilestoneSubmission, 
    ProjectStudentAssignment, User
)
from components.extensions import db

class StatisticsService:
    def get_project_statistics(self, project_id: int) -> Dict[str, Any]:
        """
        Get comprehensive project statistics including:
        - Total students
        - Overall progress
        - Submission rates
        """
        # Get total students in project
        total_students = db.session.query(func.count(ProjectStudentAssignment.student_id))\
            .filter(ProjectStudentAssignment.project_id == project_id)\
            .scalar() or 0

        # Get milestone completion stats
        milestones = Milestone.query.filter_by(project_id=project_id).all()
        total_milestones = len(milestones)
        
        if total_milestones == 0 or total_students == 0:
            return {
                "total_students": total_students,
                "total_milestones": total_milestones,
                "overall_progress": 0,
                "submission_rate": 0
            }

        # Calculate overall progress
        completion_stats = self._calculate_completion_stats(project_id)
        
        return {
            "total_students": total_students,
            "total_milestones": total_milestones,
            "overall_progress": completion_stats['overall_progress'],
            "submission_rate": completion_stats['submission_rate'],
            "milestone_completion": completion_stats['milestone_completion'],
            "submission_trends": self._get_submission_trends(project_id),
            "student_progress": self._get_student_progress(project_id)
        }

    def get_milestone_statistics(self, project_id: int) -> List[Dict[str, Any]]:
        """Get detailed statistics for each milestone."""
        milestones = Milestone.query.filter_by(project_id=project_id).all()
        total_students = self._get_total_students(project_id)

        milestone_stats = []
        for milestone in milestones:
            stats = self._get_single_milestone_stats(milestone.milestone_id, total_students)
            milestone_stats.append({
                "milestone_id": milestone.milestone_id,
                "title": milestone.title,
                "total_submissions": stats['total_submissions'],
                "approved_submissions": stats['approved_submissions'],
                "pending_submissions": stats['pending_submissions'],
                "not_submitted": stats['not_submitted'],
                "completion_rate": stats['completion_rate'],
                "submission_rate": stats['submission_rate']
            })

        return milestone_stats

    def _calculate_completion_stats(self, project_id: int) -> Dict[str, float]:
        """Calculate overall completion statistics."""
        # Get all milestones and their submissions
        milestones = Milestone.query.filter_by(project_id=project_id).all()
        total_students = self._get_total_students(project_id)
        
        if not milestones or not total_students:
            return {
                "overall_progress": 0,
                "submission_rate": 0,
                "milestone_completion": []
            }

        total_possible = len(milestones) * total_students
        total_completed = 0
        total_submitted = 0
        milestone_completion = []

        for milestone in milestones:
            stats = self._get_single_milestone_stats(milestone.milestone_id, total_students)
            total_completed += stats['approved_submissions']
            total_submitted += stats['total_submissions']
            
            milestone_completion.append({
                "milestone_id": milestone.milestone_id,
                "title": milestone.title,
                "completion_rate": stats['completion_rate']
            })

        return {
            "overall_progress": (total_completed / total_possible) * 100 if total_possible > 0 else 0,
            "submission_rate": (total_submitted / total_possible) * 100 if total_possible > 0 else 0,
            "milestone_completion": milestone_completion
        }

    def _get_single_milestone_stats(self, milestone_id: int, total_students: int) -> Dict[str, Any]:
        """Get statistics for a single milestone."""
        submissions = MilestoneSubmission.query.filter_by(milestone_id=milestone_id).all()
        
        total_submissions = len(submissions)
        approved_submissions = sum(1 for s in submissions if s.evaluation_status == 'approved')
        pending_submissions = sum(1 for s in submissions if s.evaluation_status == 'pending')
        not_submitted = total_students - total_submissions

        return {
            "total_submissions": total_submissions,
            "approved_submissions": approved_submissions,
            "pending_submissions": pending_submissions,
            "not_submitted": not_submitted,
            "completion_rate": (approved_submissions / total_students) * 100 if total_students > 0 else 0,
            "submission_rate": (total_submissions / total_students) * 100 if total_students > 0 else 0
        }

    def _get_total_students(self, project_id: int) -> int:
        """Get total number of students in a project."""
        return db.session.query(func.count(ProjectStudentAssignment.student_id))\
            .filter(ProjectStudentAssignment.project_id == project_id)\
            .scalar() or 0

    def _get_submission_trends(self, project_id: int) -> List[Dict[str, Any]]:
        """Get submission trends over time."""
        submissions = db.session.query(
            func.date(MilestoneSubmission.submission_date).label('date'),
            func.count(MilestoneSubmission.submission_id).label('count')
        ).join(Milestone)\
        .filter(Milestone.project_id == project_id)\
        .group_by(func.date(MilestoneSubmission.submission_date))\
        .order_by(func.date(MilestoneSubmission.submission_date))\
        .all()

        return [{
            "date": str(row.date),
            "submissions": row.count
        } for row in submissions]

    def _get_student_progress(self, project_id: int) -> List[Dict[str, Any]]:
        """Get individual student progress."""
        students = db.session.query(User)\
            .join(ProjectStudentAssignment)\
            .filter(ProjectStudentAssignment.project_id == project_id)\
            .all()

        student_progress = []
        total_milestones = Milestone.query.filter_by(project_id=project_id).count()

        for student in students:
            completed_milestones = db.session.query(func.count(MilestoneSubmission.submission_id))\
                .join(Milestone)\
                .filter(
                    Milestone.project_id == project_id,
                    MilestoneSubmission.student_id == student.user_id,
                    MilestoneSubmission.evaluation_status == 'approved'
                ).scalar() or 0

            progress_percentage = (completed_milestones / total_milestones * 100) if total_milestones > 0 else 0

            student_progress.append({
                "student_id": student.user_id,
                "name": student.username,
                "completed_milestones": completed_milestones,
                "progress_percentage": progress_percentage
            })

        return student_progress