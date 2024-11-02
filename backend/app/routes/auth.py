from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from flask_security import hash_password, verify_password
from ..models.models import db, User
from ..utils.helpers import generate_response, handle_error

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(email=data.get('email')).first()
        
        if user and verify_password(data.get('password'), user.password):
            login_user(user)
            return generate_response(
                data={
                    'user_id': user.user_id,
                    'email': user.email,
                    'roles': [role.name for role in user.roles]
                },
                message='Login successful'
            )
        return generate_response(message='Invalid credentials', status=401)
    except Exception as e:
        return handle_error(e)

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    try:
        logout_user()
        return generate_response(message='Logout successful')
    except Exception as e:
        return handle_error(e)

@auth_bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    try:
        return generate_response(data={
            'user_id': current_user.user_id,
            'email': current_user.email,
            'username': current_user.username,
            'roles': [role.name for role in current_user.roles],
            'created_at': current_user.created_at,
            'last_login': current_user.last_login_at
        })
    except Exception as e:
        return handle_error(e)

@auth_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    try:
        data = request.get_json()
        if not verify_password(data.get('current_password'), current_user.password):
            return generate_response(message='Current password is incorrect', status=400)
            
        current_user.password = hash_password(data.get('new_password'))
        db.session.commit()
        return generate_response(message='Password updated successfully')
    except Exception as e:
        return handle_error(e)