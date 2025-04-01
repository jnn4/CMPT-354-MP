from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import Person
from models import User
from models import Staff
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

    # Check if email already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already registered'}), 400

    # Create a new Person record
    new_person = Person(
        email=data['email'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone_num=data.get('phone_num'),
        age=data.get('age')
    )
    db.session.add(new_person)

    # Create a new User record
    new_user = User(
        email=new_person.email,
    )
    new_user.set_password(data['password'])  # Hash and store the password using pbkdf2:sha256
    db.session.add(new_user)

    db.session.commit()

    return jsonify({'message': 'Signup successful'}), 201

# Login route
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if not user or not user.check_password(data['password']):  # Use check_password() method
        return jsonify({'message': 'Invalid credentials'}), 401

    return jsonify({
        'message': 'Login successful',
        'name': f"{user.person.first_name} {user.person.last_name}",  # Get name from Person
        'email': user.email,
        'role': 'user'  # Add role logic if needed
    }), 200

@auth_bp.route('/login', methods=['OPTIONS'])
def options_login():
    return '', 200  # For CORS preflight

# Logout route
@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200
