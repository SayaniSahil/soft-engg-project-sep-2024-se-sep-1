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
    return {"token": user.get_auth_token(), "username": user.username, "email": user.email, "role": str(user.roles[0].name), "id": user.user_id}, 200

@auth_bp.route('/login_user', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        return check_user(email, password)
    except Exception as e:
        return handle_error(e)

@auth_bp.route('/register_instructor', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        username = data.get('username')
        role = "Instructor"
        if not email or not password or not username or not role:
            return jsonify({"message": "Missing required fields"}), 400
        if datastore.find_user(email=email):
            return jsonify({"message": "User already exists"}), 400
        password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = datastore.create_user(email=email, password=password, username=username)
        user.roles.append(datastore.find_role(role))
        db.session.commit()
        return {"token": user.get_auth_token(), "username": user.username, "email": user.email, "role": str(user.roles[0].name)}, 200
    except Exception as e:
        return handle_error(e)