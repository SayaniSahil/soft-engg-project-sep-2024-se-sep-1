from flask import Blueprint, request, jsonify
from flask_security import current_user, auth_required
from components.models import ProjectStudentAssignment, db
from datetime import datetime

# Create Blueprint
assignment_bp = Blueprint('assignment', __name__)

# POST: Create a new assignment with github_url
@assignment_bp.route('/assignment', methods=['POST'])
  # Ensures only authenticated users can access
def create_assignment():
    try:
        data = request.get_json()
        project_id = data.get("project_id")
        github_url = data.get("github_url")

        # Validate input
        if not project_id or not github_url:
            return jsonify({"error": "project_id and github_url are required"}), 400

        # Fetch the current user's ID
        student_id = 3

        # Check if the assignment already exists
        existing_assignment = ProjectStudentAssignment.query.filter_by(
            project_id=project_id, student_id=student_id
        ).first()

        if existing_assignment:
            return jsonify({
                "error": "Assignment already exists",
                "project_id": project_id,
                "student_id": student_id,
                "github_url": existing_assignment.github_url
            }), 409

        # Create a new assignment
        new_assignment = ProjectStudentAssignment(
            project_id=project_id,
            student_id=student_id,
            github_url=github_url,
            assigned_date=datetime.utcnow()
        )

        db.session.add(new_assignment)
        db.session.commit()

        return jsonify({
            "message": "Assignment created successfully",
            "project_id": project_id,
            "student_id": student_id,
            "github_url": github_url
        }), 201

    except Exception as e:
        print(f"Error creating assignment: {e}")
        return jsonify({"error": "An error occurred while creating the assignment"}), 500
# PUT: Update the github_url for an existing assignment
# @assignment_bp.route('/assignment/<int:project_id>', methods=['PUT'])
# @auth_required()  # Ensures only authenticated users can access
# def update_github_url(project_id):
#     try:
#         data = request.get_json()
#         new_github_url = data.get("github_url")

#         # Validate input
#         if not new_github_url:
#             return jsonify({"error": "github_url is required"}), 400

#         # Fetch the current user's ID
#         student_id = current_user.id

#         # Check if the assignment exists
#         assignment = ProjectStudentAssignment.query.filter_by(
#             project_id=project_id, student_id=student_id
#         ).first()

#         if not assignment:
#             return jsonify({"error": "Assignment not found"}), 404

#         # Update the GitHub URL
#         assignment.github_url = new_github_url
#         db.session.commit()

#         return jsonify({
#             "message": "GitHub URL updated successfully",
#             "project_id": project_id,
#             "student_id": student_id,
#             "github_url": new_github_url
#         }), 200

#     except Exception as e:
#         print(f"Error updating GitHub URL: {e}")
#         return jsonify({"error": "An error occurred while updating the GitHub URL"}), 500

# DELETE: Remove the github_url for an existing assignment
# @assignment_bp.route('/assignment/<int:project_id>', methods=['DELETE'])
# @auth_required()  # Ensures only authenticated users can access
# def delete_github_url(project_id):
#     try:
#         # Fetch the current user's ID
#         student_id = current_user.id

#         # Check if the assignment exists
#         assignment = ProjectStudentAssignment.query.filter_by(
#             project_id=project_id, student_id=student_id
#         ).first()

#         if not assignment:
#             return jsonify({"error": "Assignment not found"}), 404

#         # Remove the GitHub URL
#         assignment.github_url = None
#         db.session.commit()

#         return jsonify({
#             "message": "GitHub URL deleted successfully",
#             "project_id": project_id,
#             "student_id": student_id
#         }), 200

#     except Exception as e:
#         print(f"Error deleting GitHub URL: {e}")
#         return jsonify({"error": "An error occurred while deleting the GitHub URL"}), 500
