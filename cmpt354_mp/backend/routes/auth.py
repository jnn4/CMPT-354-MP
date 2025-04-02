from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import Person
from models import User
from models import Staff
from models import Item
from models import BorrowTransaction

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

    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401

    # Fetch additional details from Person table
    person = Person.query.filter_by(email=user.email).first()

    return jsonify({
        'message': 'Login successful',
        'email': user.email,
        'role': 'staff' if isinstance(user, Staff) else 'user',  # Example role logic
        'first_name': person.first_name,
        'last_name': person.last_name,
        'phone_num': person.phone_num,
        'age': person.age
    }), 200


@auth_bp.route('/login', methods=['OPTIONS'])
def options_login():
    return '', 200  # For CORS preflight

# Logout route
@auth_bp.route('/logout', methods=['POST'])
def logout():
    # Clear session data (if using Flask sessions)
    session.clear()

    # Respond with success message
    return jsonify({"message": "Logged out successfully"}), 200

# ---User Dashboard---
@auth_bp.route('/dashboard', methods=['GET'])
def get_user_dashboard():
    email = request.args.get('email')
    
    if not email:
        return jsonify({'message': 'Email parameter is required'}), 400

    # Join Person and User tables
    user_data = db.session.query(Person, User).join(User, Person.email == User.email).filter(Person.email == email).first()
    
    if not user_data:
        return jsonify({'message': 'User not found'}), 404
    
    person, user = user_data

    # Fetch borrowed items with a join
    borrowed_items = db.session.query(Item, BorrowTransaction).join(BorrowTransaction, Item.item_id == BorrowTransaction.item_id).filter(BorrowTransaction.user_email == email).filter(BorrowTransaction.return_date == None).all()
    
    items_list = [{
        'id': item.item_id,
        'title': item.title,
        'author': item.author,
        'pub_year': item.pub_year,
        'status': item.status,
        'borrow_date': transaction.borrow_date.strftime('%Y-%m-%d'),
        'due_date': transaction.due_date.strftime('%Y-%m-%d')
    } for item, transaction in borrowed_items]
    
    return jsonify({
        'user': {
            'firstName': person.first_name,
            'lastName': person.last_name,
            'email': person.email
        },
        'borrowedItems': items_list,
        'upcomingEvents': [],  # Add event query here
        'volunteeringPosition': None  # Add volunteer query here
    }), 200

