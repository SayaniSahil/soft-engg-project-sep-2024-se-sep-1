# backend/app/utils/helpers.py

from functools import wraps
from flask import jsonify
from flask_login import current_user
from datetime import datetime

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or 'admin' not in [role.name for role in current_user.roles]:
            return jsonify({'message': 'Admin privileges required'}), 403
        return f(*args, **kwargs)
    return decorated_function

def instructor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or 'instructor' not in [role.name for role in current_user.roles]:
            return jsonify({'message': 'Instructor privileges required'}), 403
        return f(*args, **kwargs)
    return decorated_function

def generate_response(data=None, message=None, status=200):
    response = {}
    if data is not None:
        response['data'] = data
    if message is not None:
        response['message'] = message
    return jsonify(response), status

def handle_error(e):
    return jsonify({'message': str(e)}), 400

def format_datetime(dt):
    if isinstance(dt, datetime):
        return dt.isoformat()
    return dt