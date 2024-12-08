from flask import Blueprint, request, jsonify, abort
from flask_security import auth_required, current_user
from components.models import ProjectStudentAssignment, User, db
import requests
import os

# Create Blueprint
commit_history_bp = Blueprint('commit_history', __name__)

# GitHub API base URL
GITHUB_API_BASE_URL = 'https://api.github.com/repos'

# Fetch the GitHub token from environment variables (ensure you set this in your environment)
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Helper function to fetch commit history from GitHub
def fetch_commit_history(github_url):
    # if not GITHUB_TOKEN:
    #     print("Error: GitHub token is not set in the environment variables.")
    #     return None

    # Extract username and repo name from GitHub URL
    try:
        parts = github_url.strip('/').split('/')
        owner, repo = parts[-2], parts[-1]
        print(f"Extracted Owner: {owner}, Repo: {repo}")
    except IndexError as e:
        print(f"Error parsing GitHub URL: {github_url} | Error: {e}")
        return None

    api_url = f'{GITHUB_API_BASE_URL}/{owner}/{repo}/commits'
    print(f"GitHub API URL: {api_url}")

    # Make the API request
    response = requests.get(api_url)
    print(f"GitHub API Response Status Code: {response.status_code}")

    if response.status_code == 200:
        try:
            commits = response.json()
            print(f"Fetched {len(commits)} commits from GitHub.")
            return [
                {
                    "author_name": commit["commit"]["committer"]["name"],
                    "timestamp": commit["commit"]["committer"]["date"],
                    "commit_url": commit["html_url"],
                }
                for commit in commits
            ]
        except Exception as e:
            print(f"Error processing commits data: {e}")
            return None
    else:
        print(f"Error fetching commit history: {response.text}")
        return None

# API to get commit history for the current student
@commit_history_bp.route('/commit_history/<int:student_id>/<int:project_id>', methods=['GET'])
@auth_required('token')  # Ensures the user is authenticated
def get_commit_history(student_id, project_id):
    try:
        print(f"Fetching project for Student ID: {student_id}")

        # Fetch project ID and GitHub URL for the given student_id
        project = ProjectStudentAssignment.query.filter_by(student_id=student_id, project_id=project_id).first()
        if not project: return jsonify({"error": "Project not found"}), 404
        github_url = project.github_url

        if not github_url:
            print(f"No GitHub URL found for Student ID: {student_id}")
            return jsonify({"error": "GitHub URL is missing for this student"}), 400

        print(f"Fetching commit history for GitHub URL: {github_url}")

        # Fetch commit history using a helper function
        commit_history = fetch_commit_history(github_url)
        if commit_history is None:
            return jsonify({"error": "Failed to fetch commit history from GitHub"}), 500

        print(f"Commit history fetched successfully for Student ID: {student_id}, Project ID: {project_id}")

        # Return the commit history
        return jsonify({
            "student_id": student_id,
            "project_id": project_id,
            "commit_history": commit_history
        }), 200

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


@commit_history_bp.route('/commit_history/<int:student_id>/<int:project_id>', methods=['POST'])
@auth_required('token')
def uploadURL(student_id, project_id):
    try:
        print(f"Fetching project for Student ID: {student_id}")

        # Fetch project ID and GitHub URL for the given student_id
        project = ProjectStudentAssignment.query.filter_by(student_id=student_id, project_id=project_id).first()
        if not project:
            return jsonify({"error": "Project not found"}), 404
        
        if not request.json or 'url' not in request.json:
            return jsonify({"error": "GitHub URL is missing in the request body"}), 400
        project.github_url = request.json['url']
        db.session.commit()
        return jsonify({"message": "GitHub URL updated successfully"}), 200
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500