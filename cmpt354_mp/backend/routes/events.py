from flask import Blueprint, request, jsonify
from datetime import datetime
from models import Event, User, attends, Room
from extensions import db
from sqlalchemy.orm import joinedload

events_bp = Blueprint('events', __name__)

# Get all events
@events_bp.route('/', methods=['GET'])
def get_events():
    try:
        # Get query parameters
        search_query = request.args.get('search', '').strip()
        event_type = request.args.get('type', None)

        # Start with a base query
        query = Event.query.options(joinedload(Event.room))

        # Filter by search text if provided
        if search_query:
            query = query.filter(Event.name.ilike(f"%{search_query}%"))

        # Filter by event type if provided
        if event_type and event_type != 'all':
            query = query.filter_by(type=event_type)

        # Fetch filtered events
        events = query.all()

        # Serialize event data with room details
        event_data = [{
            "event_id": event.event_id,
            "name": event.name,
            "type": event.type,
            "date": event.date.isoformat(),  # Convert date to string
            "time": event.time.strftime('%H:%M'),  # Convert time to string
            "audience_type": event.audience_type,
            "room": {
                "room_id": event.room.room_id,
                "name": event.room.name,
                "capacity": event.room.capacity
            } if event.room else None
        } for event in events]

        return jsonify(event_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Attend an event
@events_bp.route('/attend', methods=['POST'])
def attend_event():
    data = request.json
    user_email = data.get('user_email')
    event_id = data.get('event_id')

    if not user_email or not event_id:
        return jsonify({'message': 'Missing user_email or event_id'}), 400

    try:
        # Check if the user is already attending the event
        existing_attendance = db.session.query(attends).filter_by(user_email=user_email, event_id=event_id).first()
        if existing_attendance:
            return jsonify({'message': 'User is already attending this event'}), 400

        # Add user to the attendance list
        db.session.execute(attends.insert().values(
            user_email=user_email,
            event_id=event_id,
            attendance_status='registered',
            registration_date=datetime.utcnow()
        ))
        db.session.commit()

        return jsonify({'message': 'Successfully registered for the event'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

# Update attendance status
@events_bp.route('/update-status', methods=['PATCH'])
def update_attendance_status():
    data = request.json
    user_email = data.get('user_email')
    event_id = data.get('event_id')
    new_status = data.get('attendance_status')

    if not user_email or not event_id or not new_status:
        return jsonify({'message': 'Missing required fields'}), 400

    try:
        # Update attendance status in the association table
        db.session.execute(attends.update().where(
            (attends.c.user_email == user_email) & (attends.c.event_id == event_id)
        ).values(attendance_status=new_status))
        
        db.session.commit()
        return jsonify({'message': 'Attendance status updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

# POPULATING EVENTS
@events_bp.route('/populate', methods=['POST'])
def populate_events():
    try:
        # Hardcoded test events
        events = [
            {
                "name": "Python Workshop",
                "type": "workshop",
                "date": "2025-05-15",
                "time": "14:00",
                "room_id": 1,  # Ensure this room exists in your database
                "audience_type": "developers"
            },
            {
                "name": "Book Club Meeting",
                "type": "meetup",
                "date": "2025-05-20",
                "time": "18:30",
                "room_id": 2,
                "audience_type": "readers"
            },
            {
                "name": "Tech Career Seminar",
                "type": "seminar",
                "date": "2025-05-25",
                "time": "10:00",
                "room_id": 3,
                "audience_type": "students"
            }
        ]

        # Insert events
        for event in events:
            new_event = Event(
                name=event["name"],
                type=event["type"],
                date=datetime.strptime(event["date"], '%Y-%m-%d').date(),
                time=datetime.strptime(event["time"], '%H:%M').time(),
                room_id=event["room_id"],
                audience_type=event["audience_type"]
            )
            db.session.add(new_event)
        
        db.session.commit()
        return jsonify({"message": f"{len(events)} events populated successfully!"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@events_bp.route('/unregister', methods=['POST'])
def unregister_event():
    data = request.json
    email = data.get('user_email')
    event_id = data.get('event_id')

    try:
        # Delete attendance record
        db.session.execute(
            attends.delete().where(
                (attends.c.user_email == email) &
                (attends.c.event_id == event_id)
            )
        )
        db.session.commit()
        return jsonify({'message': 'Successfully unregistered from event'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500


# Create an event
@events_bp.route('/create', methods=['POST'])
def create_event():
    data = request.json

    room = Room.query.get(data['room_id'])
    if not room:
        return jsonify({"message": "Room not found"}), 404

    try:
        new_event = Event(
            name=data['name'],
            type=data['type'],
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            time=datetime.strptime(data['time'], '%H:%M').time(),
            room_id=data['room_id'],
            audience_type=data['audience_type']
        )
        
        db.session.add(new_event)
        db.session.commit()
        
        return jsonify({"message": "Event created successfully!", "event_id": new_event.event_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


def _build_cors_preflight_response():
    response = jsonify({'message': 'CORS preflight'})
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "DELETE, OPTIONS")
    return response

# Delete an event
@events_bp.route('/delete/<int:event_id>', methods=['DELETE', 'OPTIONS'])
def delete_event(event_id):
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()

    try:
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"message": "Event not found"}), 404

        db.session.delete(event)
        db.session.commit()
        
        return jsonify({"message": "Event deleted successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@events_bp.route('/populate_rooms', methods=['POST'])
def populate_rooms():
    try:
        data = request.json.get('rooms', [])
        
        for room in data:
            new_room = Room(
                name=room['name'],
                capacity=room['capacity']
            )
            db.session.add(new_room)

        db.session.commit()
        return jsonify({'message': f'{len(data)} rooms populated successfully!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# get all rooms
@events_bp.route('/rooms', methods=['GET'])
def get_rooms():
    try:
        rooms = Room.query.all()
        return jsonify([{
            "room_id": room.room_id,
            "name": room.name,
            "capacity": room.capacity
        } for room in rooms]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
