from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from flask_security import roles_required
from sqlalchemy import and_, or_, desc
from datetime import datetime, timedelta
import requests
import hmac
import hashlib
import json
from urllib.parse import urlparse

from ..models.models import (
    db, GithubIntegration, GithubCommit, Student, 
    Project, ProjectStudentAssignment
)
from ..utils.helpers import generate_response, handle_error

github_bp = Blueprint('github', __name__)

# GitHub API configuration
GITHUB_API_URL = "https://api.github.com"
GITHUB_WEBHOOK_SECRET = current_app.config.get('GITHUB_WEBHOOK_SECRET', '')
GITHUB_ACCESS_TOKEN = current_app.config.get('GITHUB_ACCESS_TOKEN', '')

def verify_github_webhook(request_data, signature):
    """Verify GitHub webhook signature"""
    expected_signature = 'sha1=' + hmac.new(
        GITHUB_WEBHOOK_SECRET.encode(),
        request_data,
        hashlib.sha1
    ).hexdigest()
    return hmac.compare_digest(expected_signature, signature)

def get_github_headers():
    """Get headers for GitHub API requests"""
    return {
        'Authorization': f'token {GITHUB_ACCESS_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }

@github_bp.route('/repository/link', methods=['POST'])
@login_required
def link_repository():
    """Link GitHub repository to student project"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['project_id', 'repository_url']
        for field in required_fields:
            if field not in data:
                return generate_response(
                    message=f'Missing required field: {field}',
                    status=400
                )

        # Verify project assignment
        assignment = ProjectStudentAssignment.query.filter_by(
            project_id=data['project_id'],
            student_id=current_user.user_id
        ).first()
        if not assignment:
            return generate_response(message='Project not assigned to student', status=403)

        # Parse repository URL
        parsed_url = urlparse(data['repository_url'])
        if 'github.com' not in parsed_url.netloc:
            return generate_response(message='Invalid GitHub repository URL', status=400)
        
        path_parts = parsed_url.path.strip('/').split('/')
        if len(path_parts) != 2:
            return generate_response(message='Invalid repository URL format', status=400)
        
        owner, repo_name = path_parts

        # Verify repository exists and is accessible
        repo_url = f"{GITHUB_API_URL}/repos/{owner}/{repo_name}"
        response = requests.get(repo_url, headers=get_github_headers())
        if response.status_code != 200:
            return generate_response(message='Repository not found or inaccessible', status=400)

        # Create or update integration
        integration = GithubIntegration.query.filter_by(
            student_id=current_user.user_id,
            project_id=data['project_id']
        ).first()

        if integration:
            integration.repository_url = data['repository_url']
            integration.repository_name = repo_name
            integration.last_sync_timestamp = datetime.utcnow()
        else:
            integration = GithubIntegration(
                student_id=current_user.user_id,
                project_id=data['project_id'],
                repository_url=data['repository_url'],
                repository_name=repo_name,
                last_sync_timestamp=datetime.utcnow()
            )
            db.session.add(integration)

        # Set up webhook
        webhook_url = f"{request.host_url.rstrip('/')}/api/github/webhook"
        webhook_data = {
            'name': 'web',
            'active': True,
            'events': ['push'],
            'config': {
                'url': webhook_url,
                'content_type': 'json',
                'secret': GITHUB_WEBHOOK_SECRET
            }
        }
        
        webhook_response = requests.post(
            f"{repo_url}/hooks",
            headers=get_github_headers(),
            json=webhook_data
        )

        if webhook_response.status_code == 201:
            integration.webhook_enabled = True

        db.session.commit()

        return generate_response(
            message='Repository linked successfully',
            data={'integration_id': integration.integration_id}
        )
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@github_bp.route('/webhook', methods=['POST'])
def github_webhook():
    """Handle GitHub webhook events"""
    try:
        # Verify webhook signature
        signature = request.headers.get('X-Hub-Signature')
        if not signature or not verify_github_webhook(request.get_data(), signature):
            return generate_response(message='Invalid signature', status=403)

        event_type = request.headers.get('X-GitHub-Event')
        if event_type != 'push':
            return generate_response(message='Event not handled', status=200)

        data = request.get_json()
        
        # Extract repository information
        repo_url = data['repository']['html_url']
        integration = GithubIntegration.query.filter_by(
            repository_url=repo_url
        ).first()
        
        if not integration:
            return generate_response(message='Repository not found', status=404)

        # Process commits
        for commit_data in data['commits']:
            existing_commit = GithubCommit.query.filter_by(
                commit_id=commit_data['id']
            ).first()
            
            if not existing_commit:
                commit = GithubCommit(
                    commit_id=commit_data['id'],
                    integration_id=integration.integration_id,
                    commit_message=commit_data['message'],
                    commit_timestamp=datetime.fromisoformat(commit_data['timestamp']),
                    commit_url=commit_data['url'],
                    files_changed=len(commit_data['added']) + len(commit_data['removed']) + len(commit_data['modified']),
                    insertions=commit_data.get('stats', {}).get('additions', 0),
                    deletions=commit_data.get('stats', {}).get('deletions', 0)
                )
                db.session.add(commit)

        integration.last_sync_timestamp = datetime.utcnow()
        db.session.commit()

        return generate_response(message='Webhook processed successfully')
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

@github_bp.route('/commits/<string:student_id>', methods=['GET'])
@login_required
def get_commits(student_id):
    """Get student's commit history"""
    try:
        # Verify access permissions
        if not current_user.has_role('admin') and \
           not current_user.has_role('instructor') and \
           current_user.user_id != student_id:
            return generate_response(message='Access denied', status=403)

        # Get query parameters
        project_id = request.args.get('project_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))

        # Base query
        query = GithubCommit.query\
            .join(GithubIntegration)\
            .filter(GithubIntegration.student_id == student_id)

        if project_id:
            query = query.filter(GithubIntegration.project_id == project_id)
        if start_date:
            query = query.filter(GithubCommit.commit_timestamp >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(GithubCommit.commit_timestamp <= datetime.fromisoformat(end_date))

        # Order by timestamp
        query = query.order_by(desc(GithubCommit.commit_timestamp))

        # Pagination
        paginated_commits = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        return generate_response(data={
            'commits': [{
                'commit_id': commit.commit_id,
                'message': commit.commit_message,
                'timestamp': commit.commit_timestamp.isoformat(),
                'url': commit.commit_url,
                'files_changed': commit.files_changed,
                'insertions': commit.insertions,
                'deletions': commit.deletions
            } for commit in paginated_commits.items],
            'total': paginated_commits.total,
            'pages': paginated_commits.pages,
            'current_page': page
        })
    except Exception as e:
        return handle_error(e)

@github_bp.route('/analytics/<string:student_id>', methods=['GET'])
@login_required
def get_commit_analytics(student_id):
    """Get analytics about student's GitHub activity"""
    try:
        # Verify access permissions
        if not current_user.has_role('admin') and \
           not current_user.has_role('instructor') and \
           current_user.user_id != student_id:
            return generate_response(message='Access denied', status=403)

        project_id = request.args.get('project_id')
        
        # Base query
        base_query = GithubCommit.query\
            .join(GithubIntegration)\
            .filter(GithubIntegration.student_id == student_id)

        if project_id:
            base_query = base_query.filter(GithubIntegration.project_id == project_id)

        # Get date range
        first_commit = base_query.order_by(GithubCommit.commit_timestamp).first()
        last_commit = base_query.order_by(desc(GithubCommit.commit_timestamp)).first()

        if not first_commit or not last_commit:
            return generate_response(message='No commits found')

        # Calculate various metrics
        total_commits = base_query.count()
        total_files_changed = db.session.query(db.func.sum(GithubCommit.files_changed))\
            .select_from(base_query.subquery())\
            .scalar() or 0
        total_insertions = db.session.query(db.func.sum(GithubCommit.insertions))\
            .select_from(base_query.subquery())\
            .scalar() or 0
        total_deletions = db.session.query(db.func.sum(GithubCommit.deletions))\
            .select_from(base_query.subquery())\
            .scalar() or 0

        # Get commit frequency by day
        commit_frequency = db.session.query(
            db.func.date(GithubCommit.commit_timestamp),
            db.func.count(GithubCommit.commit_id)
        ).select_from(base_query.subquery())\
        .group_by(db.func.date(GithubCommit.commit_timestamp))\
        .all()

        # Calculate activity patterns
        activity_hours = db.session.query(
            db.func.extract('hour', GithubCommit.commit_timestamp),
            db.func.count(GithubCommit.commit_id)
        ).select_from(base_query.subquery())\
        .group_by(db.func.extract('hour', GithubCommit.commit_timestamp))\
        .all()

        return generate_response(data={
            'overview': {
                'total_commits': total_commits,
                'total_files_changed': total_files_changed,
                'total_insertions': total_insertions,
                'total_deletions': total_deletions,
                'first_commit': first_commit.commit_timestamp.isoformat(),
                'last_commit': last_commit.commit_timestamp.isoformat()
            },
            'commit_frequency': {
                str(date): count for date, count in commit_frequency
            },
            'activity_pattern': {
                str(int(hour)): count for hour, count in activity_hours
            },
            'avg_commits_per_day': round(
                total_commits / ((last_commit.commit_timestamp - first_commit.commit_timestamp).days + 1),
                2
            ) if total_commits > 0 else 0
        })
    except Exception as e:
        return handle_error(e)

@github_bp.route('/repository/<string:integration_id>', methods=['DELETE'])
@login_required
def unlink_repository(integration_id):
    """Unlink GitHub repository"""
    try:
        integration = GithubIntegration.query.get_or_404(integration_id)
        
        # Verify ownership
        if integration.student_id != current_user.user_id:
            return generate_response(message='Access denied', status=403)

        # Remove webhook if enabled
        if integration.webhook_enabled:
            parsed_url = urlparse(integration.repository_url)
            path_parts = parsed_url.path.strip('/').split('/')
            owner, repo_name = path_parts
            
            # Get webhooks
            hooks_url = f"{GITHUB_API_URL}/repos/{owner}/{repo_name}/hooks"
            response = requests.get(hooks_url, headers=get_github_headers())
            
            if response.status_code == 200:
                hooks = response.json()
                for hook in hooks:
                    if hook['config']['url'].endswith('/api/github/webhook'):
                        requests.delete(
                            f"{hooks_url}/{hook['id']}",
                            headers=get_github_headers()
                        )

        # Delete all commits
        GithubCommit.query.filter_by(integration_id=integration_id).delete()
        
        # Delete integration
        db.session.delete(integration)
        db.session.commit()

        return generate_response(message='Repository unlinked successfully')
    except Exception as e:
        db.session.rollback()
        return handle_error(e)

# Error handlers
@github_bp.errorhandler(404)
def not_found_error(error):
    return generate_response(message='Resource not found', status=404)

@github_bp.errorhandler(403)
def forbidden_error(error):
    return generate_response(message='Forbidden', status=403)