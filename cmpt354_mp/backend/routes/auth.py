from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from extensions import db
from flask_cors import CORS  # Ensure CORS is imported

# Create Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

# Enable CORS for all routes in the Blueprint
CORS(auth_bp, resources={r"/*": {"origins": "http://localhost:5173"}})

# Signup route
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'User already exists'}), 400

    # Create new user
    new_user = User(
        name=data['email'],  # You could change this to ask for a separate name field
        email=data['email'],
        password_hash=generate_password_hash(data['password'], method='pbkdf2:sha256'),
        role='user'
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

# Login route
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401

    return jsonify({'message': 'Login successful', 'role': user.role}), 200

@auth_bp.route('/login', methods=['OPTIONS'])
def options_login():
    return '', 200  # For CORS preflight

# Logout route
@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200
