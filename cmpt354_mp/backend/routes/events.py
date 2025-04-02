from flask import Blueprint, request, jsonify
from extensions import db
from models import Event, attends
from datetime import date, time

# Create a Blueprint for events
events_bp = Blueprint('events', __name__, url_prefix='/events')

# Get all events
@events_bp.route('/', methods=['GET'])
def get_events():
    events = Event.query.all()
    events_list = [{
        'event_id': event.event_id,
        'name': event.name,
        'event_type': event.event_type,
        'description': event.description,
        'date': event.date.strftime('%Y-%m-%d'),
        'time': event.time.strftime('%H:%M:%S'),
        'room_id': event.room_id
    } for event in events]
    return jsonify(events_list), 200

# Get a specific event by ID
@events_bp.route('/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = Event.query.get(event_id)
    if event:
        return jsonify({
            'event_id': event.event_id,
            'name': event.name,
            'event_type': event.event_type,
            'description': event.description,
            'date': event.date.strftime('%Y-%m-%d'),
            'time': event.time.strftime('%H:%M:%S'),
            'room_id': event.room_id
        }), 200
    return jsonify({'error': 'Event not found'}), 404

# Create a new event
@events_bp.route('/', methods=['POST'])
def create_event():
    data = request.get_json()
    new_event = Event(
        name=data['name'],
        event_type=data['event_type'],
        description=data.get('description'),
        date=data['date'],
        time=data['time'],
        room_id=data.get('room_id')
    )
    db.session.add(new_event)
    db.session.commit()
    return jsonify({'message': 'Event created successfully', 'event_id': new_event.event_id}), 201

# Update an existing event
@events_bp.route('/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    
    data = request.get_json()
    event.name = data.get('name', event.name)
    event.event_type = data.get('event_type', event.event_type)
    event.description = data.get('description', event.description)
    event.date = data.get('date', event.date)
    event.time = data.get('time', event.time)
    event.room_id = data.get('room_id', event.room_id)
    
    db.session.commit()
    return jsonify({'message': 'Event updated successfully'}), 200

# Delete an event
@events_bp.route('/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event deleted successfully'}), 200

# Populate the database with sample data
@events_bp.route('/populate_events', methods=['POST'])
def populate_events():
    try:
        events_data = [
            {
                "name": "Python Programming Workshop",
                "event_type": "Workshop",
                "description": "An interactive session on Python basics and advanced topics.",
                "date": date(2025, 4, 15),
                "time": time(14, 0),
                "room_id": 1
            },
            {
                "name": "Book Club: '1984' by George Orwell",
                "event_type": "Book Club",
                "description": "A discussion on George Orwell's novel *1984*.",
                "date": date(2025, 4, 18),
                "time": time(17, 30),
                "room_id": 2
            },
            {
                "name": "Guest Lecture: The Future of AI",
                "event_type": "Lecture",
                "description": "A talk by Dr. Jane Smith on AI and its ethical implications.",
                "date": date(2025, 4, 22),
                "time": time(16, 0),
                "room_id": 3
            },
            {
                "name": "Children's Storytime",
                "event_type": "Reading",
                "description": "A fun storytelling session for kids aged 4-8.",
                "date": date(2025, 4, 25),
                "time": time(10, 0),
                "room_id": 1
            },
            {
                "name": "Poetry Night",
                "event_type": "Performance",
                "description": "An open mic night for poetry lovers.",
                "date": date(2025, 4, 30),
                "time": time(19, 0),
                "room_id": 2
            },
            {
                "name": "Local Author Meet & Greet",
                "event_type": "Author Talk",
                "description": "Meet and interact with bestselling local authors.",
                "date": date(2025, 5, 3),
                "time": time(15, 0),
                "room_id": 3
            },
            {
                "name": "History Lecture: The Renaissance",
                "event_type": "Lecture",
                "description": "A deep dive into the Renaissance period and its impact on modern society.",
                "date": date(2025, 5, 7),
                "time": time(16, 30),
                "room_id": 4
            },
            {
                "name": "Film Screening: 'The Great Gatsby'",
                "event_type": "Movie Night",
                "description": "A screening of *The Great Gatsby* followed by a discussion.",
                "date": date(2025, 5, 10),
                "time": time(18, 0),
                "room_id": 5
            },
            {
                "name": "Workshop: Resume Building & Career Advice",
                "event_type": "Workshop",
                "description": "A session on crafting effective resumes and interview techniques.",
                "date": date(2025, 5, 12),
                "time": time(14, 0),
                "room_id": 6
            },
            {
                "name": "Music & Arts Festival",
                "event_type": "Festival",
                "description": "A celebration of music, arts, and culture with live performances.",
                "date": date(2025, 5, 20),
                "time": time(12, 0),
                "room_id": 7
            }
        ]

        for events_data in events_data:
            event = Event(**events_data)
            db.session.add(event)

        db.session.commit()
        return jsonify({"message": "Events populated successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# Register for an event
@events_bp.route('/register/<int:event_id>', methods=['POST'])
def register_for_event(event_id):
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400
            
        # Check if user is already registered
        existing_registration = db.session.query(attends).filter_by(
            user_id=user_id,
            event_id=event_id
        ).first()
        
        if existing_registration:
            return jsonify({'error': 'User is already registered for this event'}), 400
            
        # Add new registration
        db.session.execute(attends.insert().values(
            user_id=user_id,
            event_id=event_id,
            attendance_status='registered',
            registration_date=date.today()
        ))
        db.session.commit()
        
        return jsonify({'message': 'Successfully registered for event'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Get user's registered events
@events_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_events(user_id):
    try:
        # Get all events the user is registered for
        user_events = db.session.query(Event).join(attends).filter(
            attends.c.user_id == user_id
        ).all()
        
        events_list = [{
            'event_id': event.event_id,
            'name': event.name,
            'event_type': event.event_type,
            'description': event.description,
            'date': event.date.strftime('%Y-%m-%d'),
            'time': event.time.strftime('%H:%M:%S'),
            'room_id': event.room_id
        } for event in user_events]
        
        return jsonify(events_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
