# auth.py handles the login, sign up, logout and dashboard updates.
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import Person, User, Staff, Volunteer, Item, FutureItem, donates, RequestHelp
from models import BorrowTransaction, Fine
from models import Event, attends
from datetime import datetime


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

    # Validate required fields
    required_fields = ['email', 'first_name', 'last_name', 'password', 'role']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing required field: {field}'}), 400

    # Check if email already exists
    if Person.query.filter_by(email=data['email']).first():
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
    db.session.commit()  # Commit to generate person.email for foreign keys

    # Create User entry (always, regardless of role)
    new_user = User(
        email=new_person.email
    )
    new_user.set_password(data['password'])
    db.session.add(new_user)

    # Create Staff/User specific entry
    role = data['role'].lower()
    
    if role == 'staff':
        new_staff = Staff(email=new_person.email)
        db.session.add(new_staff)

    db.session.commit()

    return jsonify({'message': f'Successfully registered as {role}'}), 201


# Login route
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401

    # Fetch additional details from Person table
    person = Person.query.filter_by(email=user.email).first()

    # Check if user is also a staff member
    is_staff = Staff.query.filter_by(email=user.email).first() is not None

    return jsonify({
        'message': 'Login successful',
        'email': user.email,
        'role': 'staff' if is_staff else 'user',  # Fixed role check
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
    user_data = db.session.query(Person, User)\
        .join(User, Person.email == User.email)\
        .filter(Person.email == email)\
        .first()
    
    if not user_data:
        return jsonify({'message': 'User not found'}), 404
    
    person, user = user_data

    # Fetch borrowed items with join
    borrowed_items = db.session.query(Item, BorrowTransaction)\
        .join(BorrowTransaction, Item.item_id == BorrowTransaction.item_id)\
        .filter(BorrowTransaction.user_email == email)\
        .filter(BorrowTransaction.return_date == None)\
        .all()
    
    items_list = [{
        'id': item.item_id,
        'title': item.title,
        'author': item.author,
        'pub_year': item.pub_year,
        'status': item.status,
        'borrow_date': transaction.borrow_date.strftime('%Y-%m-%d'),
        'due_date': transaction.due_date.strftime('%Y-%m-%d')
    } for item, transaction in borrowed_items]

    # Fetch fines with item and transaction details
    fines = db.session.query(Fine, BorrowTransaction, Item)\
        .join(BorrowTransaction, Fine.trans_id == BorrowTransaction.trans_id)\
        .join(Item, BorrowTransaction.item_id == Item.item_id)\
        .filter(BorrowTransaction.user_email == email)\
        .all()

    fines_list = [{
        'fine_id': fine.fine_id,
        'amount': float(fine.amount),
        'paid': fine.paid,
        'item_title': item.title,
        'borrow_date': transaction.borrow_date.strftime('%Y-%m-%d'),
        'due_date': transaction.due_date.strftime('%Y-%m-%d'),
        'days_overdue': (datetime.utcnow() - transaction.due_date).days if datetime.utcnow() > transaction.due_date else 0
    } for fine, transaction, item in fines]

    # Fetch upcoming events with join
    upcoming_events = db.session.query(Event, attends.c.attendance_status)\
        .join(attends, Event.event_id == attends.c.event_id)\
        .filter(attends.c.user_email == email)\
        .filter(Event.date >= datetime.utcnow().date())\
        .all()
    
    events_list = [{
        'id': event.event_id,
        'name': event.name,
        'type': event.type,
        'date': event.date.isoformat(),
        'time': event.time.strftime('%H:%M'),
        'status': status,
        'location': event.room.name if event.room else 'Online'
    } for event, status in upcoming_events]

    # Fetch ALL volunteer entries
    volunteer_entries = db.session.query(Volunteer)\
        .filter_by(email=email)\
        .order_by(Volunteer.start_date.desc())\
        .all()

    volunteer_history = [{
        'start_date': entry.start_date.isoformat(),
        'end_date': entry.end_date.isoformat() if entry.end_date else None,
        'status': 'active' if not entry.end_date else 'completed'
    } for entry in volunteer_entries]

    # Fetch donated items with specific columns
    donated_items = db.session.query(
        Item,
        FutureItem,
        donates.c.donation_date,
        donates.c.donation_status
    ).join(
        donates, Item.item_id == donates.c.item_id
    ).outerjoin(
        FutureItem, Item.item_id == FutureItem.item_id
    ).filter(
        donates.c.user_email == email
    ).all()

    # Build donated items list
    donated_list = [{
        'item_id': item.item_id,
        'title': item.title,
        'author': item.author,
        'type': item.type,
        'donation_date': donation_date.strftime('%Y-%m-%d'),
        'arrival_date': future.arrival_date.strftime('%Y-%m-%d') if future else 'Arrived',
        'current_status': item.status,
        'donation_status': donation_status
    } for item, future, donation_date, donation_status in donated_items]

    # Fetch help requests for the user
    help_requests = db.session.query(RequestHelp)\
                              .filter_by(user_email=email)\
                              .order_by(RequestHelp.created_at.desc())\
                              .all()

    help_requests_list = [{
        "id": req.request_id,
        "request_text": req.request_text,
        "status": "Open" if req.status else "Closed",
        "created_at": req.created_at.isoformat()
    } for req in help_requests]

    return jsonify({
        'user': {
            'firstName': person.first_name,
            'lastName': person.last_name,
            'email': person.email
        },
        'borrowedItems': items_list,
        'fines': fines_list,
        'upcomingEvents': events_list,
        'volunteeringHistory': volunteer_history,  # Changed to array of entries
        'donatedItems': donated_list,
        'helpRequests': help_requests_list  # Added help requests data here
    }), 200

# staff dashboard
@auth_bp.route('/dashboard/staff', methods=['GET'])
def get_staff_dashboard():
    email = request.args.get('email')
    
    if not email:
        return jsonify({'message': 'Email parameter is required'}), 400

    # Join Person and Staff tables
    staff_data = db.session.query(Person, Staff)\
        .join(Staff, Person.email == Staff.email)\
        .filter(Person.email == email)\
        .first()
    
    if not staff_data:
        return jsonify({'message': 'Staff member not found'}), 404
    
    person, staff = staff_data

    return jsonify({
        'email': person.email,
        'first_name': person.first_name,
        'last_name': person.last_name,
        'phone_num': person.phone_num,
        'age': person.age,
        'wage': staff.wage,
        # Add other staff-specific fields if needed
    }), 200