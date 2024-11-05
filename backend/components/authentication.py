from flask import Blueprint, request, jsonify
from flask_security import auth_required
from components.extensions import db, bcrypt, datastore
from utils.helpers import generate_response, handle_error

auth_bp = Blueprint('auth', __name__)

def check_user(email, password):
    # Check if email and password is provided
    if not email or not password: return jsonify({"message": "Email or Password not provided"}), 400
    # Check if email is valid
    user = datastore.find_user(email=email)
    if not user: return jsonify({"message": "Email or Password is incorrect"}), 400
    # Check password hash
    match = bcrypt.check_password_hash(user.password, password)
    if not match: return jsonify({"message": "Email or Password incorrect"}), 400
    # If everything is correct, return authentication token
    return {"token": user.get_auth_token(), "email": user.email, "role": str(user.roles[0].name)}, 200

@auth_bp.route('/login_user', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        return check_user(email, password)
    except Exception as e:
        return handle_error(e)

'''@auth_bp.route('/logout_user', methods=['POST'])
#@login_required
def logout():
    try:
        logout_user()
        
        return generate_response(message='Logout successful')
    except Exception as e:
        return handle_error(e)'''

# Restrict access to only authenticated users, needs changes
@auth_bp.route('/profile', methods=['POST'])
@auth_required('token')
def get_profile():
    try:
        user = datastore.find_user(email=request.get_json().get('email'))
        return generate_response(data={
            'user_id': user.user_id,
            'email': user.email,
            'username': user.username,
            'role': str(user.roles[0].name)
        })
    except Exception as e:
        return handle_error(e)