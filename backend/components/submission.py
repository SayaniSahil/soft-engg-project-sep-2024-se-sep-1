from flask import Blueprint, request, jsonify, abort
from flask_security import auth_required
from datetime import datetime
from components.models import db, MilestoneSubmission

# Define a Blueprint for project operations
student_submission_bp = Blueprint('submission', __name__)

# class MilestoneSubmission(db.Model):
#     __tablename__ = 'milestone_submissions'
    
#     submission_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  i have included autoincrement part

@student_submission_bp.route('/submitmilestone', methods=['POST'])
def submit_milestone():
    # Parse the JSON data sent in the request
    data = request.get_json()

    # Extract fields from the incoming request
    milestone_id = data.get('milestone_id')
    student_id = data.get('student_id')
    document_url = data.get('document_url')

    # Validate required fields
    if not milestone_id or not student_id or not document_url:
        return jsonify({"message": "Missing required fields "}), 400

    # Optionally handle the evaluation date if provided
    evaluation_date = data.get('evaluation_date')
    if evaluation_date: 
        try:
            evaluation_date = datetime.strptime(evaluation_date, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return jsonify({"message": "Invalid date format"}), 400

    # Create a new instance of MilestoneSubmission without 'submission_id'
    new_submission = MilestoneSubmission(
        milestone_id=milestone_id,
        student_id=student_id,
        document_url=document_url,
        evaluation_date=evaluation_date  # It could be None if not provided
    )
    print("About to submit to database:", {
        "milestone_id": new_submission.milestone_id,
        "student_id": new_submission.student_id,
        "document_url": new_submission.document_url,
        "evaluation_date": new_submission.evaluation_date
    })
    # Add and commit to the database
    db.session.add(new_submission)
    db.session.commit()

    # After committing, the 'submission_id' will be auto-generated
    return jsonify({
        "message": "Milestone submission successful",
        "submission_id": new_submission.submission_id  # Return the auto-generated ID
    }), 201