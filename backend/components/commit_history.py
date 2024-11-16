from flask import Blueprint, request, jsonify, abort
from flask_security import auth_required
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
    if not GITHUB_TOKEN:
        print("Error: GitHub token is not set in the environment variables.")
        return None
    
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    
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
    response = requests.get(api_url, headers=headers)
    print(f"GitHub API Response Status Code: {response.status_code}")
    
    if response.status_code == 200:
        try:
            commits = response.json()
            print(f"Fetched {len(commits)} commits from GitHub.")
            # Adjusting to fetch `author name`, `timestamp`, and `commit_url` from `parents`.
            return [
                {
                    "author_name": commit["commit"]["committer"]["name"],
                    "timestamp": commit["commit"]["committer"]["date"],
                    "commit_url": commit["html_url"],  # The `html_url` directly maps to the commit link
                }
                for commit in commits
            ]
        except Exception as e:
            print(f"Error processing commits data: {e}")
            return None
    else:
        print(f"Error fetching commit history: {response.text}")
        return None


# API to get commit history for a specific student by project and student ID
@commit_history_bp.route('/commit_history/<int:project_id>/<int:student_id>', methods=['GET'])
def get_commit_history(project_id, student_id):
    # Check if student is enrolled in the project
    assignment = ProjectStudentAssignment.query.filter_by(project_id=project_id, student_id=student_id).first()
    
    if not assignment:
        print(f"Error: No assignment found for Project ID: {project_id}, Student ID: {student_id}")
        return jsonify({"error": "Student is not enrolled in this project"}), 404
    
    # Fetch commit history using the GitHub URL
    github_url = assignment.github_url
    if not github_url:
        print(f"Error: No GitHub URL found for Student ID: {student_id} in Project ID: {project_id}")
        return jsonify({"error": "GitHub URL not available for this student"}), 400
    
    print(f"Fetching commit history for GitHub URL: {github_url}")
    commit_history = fetch_commit_history(github_url)
    if commit_history is None:
        print(f"Error: Failed to fetch commit history for GitHub URL: {github_url}")
        return jsonify({"error": "Failed to fetch commit history"}), 500
    
    print(f"Commit history fetched successfully for Student ID: {student_id} in Project ID: {project_id}")
    return jsonify({
        "student_id": student_id,
        "project_id": project_id,
        "commit_history": commit_history
    }), 200
