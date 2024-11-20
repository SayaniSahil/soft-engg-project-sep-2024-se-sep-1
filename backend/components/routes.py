from flask import Blueprint, current_app
from flask_security import auth_required, roles_required, current_user
from components.extensions import db, cache
from utils.helpers import APIResponse
from .services import StatisticsService

stats_bp = Blueprint('statistics', __name__)

@stats_bp.route('/projects/<int:project_id>/statistics', methods=['GET'])
@auth_required('token')
def get_project_statistics(project_id: int):
    """Get comprehensive statistics for a specific project."""
    try:
        # Check cache first
        cache_key = f'project_statistics_{project_id}'
        cached_stats = cache.get(cache_key)
        if cached_stats:
            return APIResponse.success(data=cached_stats)

        stats_service = StatisticsService()
        project_stats = stats_service.get_project_statistics(project_id)
        
        # Cache for 5 minutes
        cache.set(cache_key, project_stats, timeout=300)
        
        return APIResponse.success(data=project_stats)
    except Exception as e:
        current_app.logger.error(f"Error fetching project statistics: {str(e)}")
        return APIResponse.error(str(e))

@stats_bp.route('/projects/<int:project_id>/milestone-statistics', methods=['GET'])
@auth_required('token')
def get_milestone_statistics(project_id: int):
    """Get detailed statistics for all milestones in a project."""
    try:
        cache_key = f'milestone_statistics_{project_id}'
        cached_stats = cache.get(cache_key)
        if cached_stats:
            return APIResponse.success(data=cached_stats)

        stats_service = StatisticsService()
        milestone_stats = stats_service.get_milestone_statistics(project_id)
        
        cache.set(cache_key, milestone_stats, timeout=300)
        
        return APIResponse.success(data=milestone_stats)
    except Exception as e:
        current_app.logger.error(f"Error fetching milestone statistics: {str(e)}")
        return APIResponse.error(str(e))