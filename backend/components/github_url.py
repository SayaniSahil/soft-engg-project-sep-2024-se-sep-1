from flask import Blueprint, request, jsonify
from flask_security import auth_required, current_user
from components.models import ProjectStudentAssignment, db
from datetime import datetime

# Create Blueprint
assignment_bp = Blueprint('assignment', __name__)

@assignment_bp.route('/assignment', methods=['POST'])
  # Ensures only authenticated users can access
def manage_assignment():
    try:
        data = request.get_json()
        github_url = data.get("github_url")

        # Validate input
        if not github_url:
            return jsonify({"error": "github_url is required"}), 400

        # Fetch the current logged-in user's ID
        student_id = 7

        # Retrieve the user's project assignment
        assignment = ProjectStudentAssignment.query.filter_by(student_id=student_id).first()

        if assignment:
            # If assignment exists, update the GitHub URL
            assignment.github_url = github_url
            assignment.assigned_date = datetime.utcnow()
            db.session.commit()

            return jsonify({
                "message": "GitHub URL updated successfully",
                "project_id": assignment.project_id,
                "student_id": student_id,
                "github_url": github_url
            }), 200
        else:
            # If no assignment exists, create a new one
            new_assignment = ProjectStudentAssignment(
                student_id=student_id,
                github_url=github_url,
                assigned_date=datetime.utcnow()
            )
            db.session.add(new_assignment)
            db.session.commit()

            return jsonify({
                "message": "GitHub URL added successfully",
                "student_id": student_id,
                "github_url": github_url
            }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

