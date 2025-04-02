from flask import Blueprint, request, jsonify
from datetime import datetime
from models import Event, User, attends
from extensions import db

events_bp = Blueprint('events', __name__)

# Get all events
@events_bp.route('/', methods=['GET'])
def get_events():
    search_query = request.args.get('search', '')
    event_type = request.args.get('type', None)

    # Filter events based on search query and type
    query = Event.query
    if search_query:
        query = query.filter(Event.name.ilike(f"%{search_query}%"))
    if event_type:
        query = query.filter_by(type=event_type)
    
    events = query.all()
    return jsonify([{
        'event_id': event.event_id,
        'name': event.name,
        'type': event.type,
        'date': event.date.isoformat(),
        'time': event.time.strftime('%H:%M'),
        'min_age': event.min_age,
        'max_age': event.max_age,
        'audience_type': event.audience_type
    } for event in events]), 200

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
                "min_age": 16,
                "max_age": 60,
                "audience_type": "developers"
            },
            {
                "name": "Book Club Meeting",
                "type": "meetup",
                "date": "2025-05-20",
                "time": "18:30",
                "room_id": 2,
                "min_age": 18,
                "max_age": 99,
                "audience_type": "readers"
            },
            {
                "name": "Tech Career Seminar",
                "type": "seminar",
                "date": "2025-05-25",
                "time": "10:00",
                "room_id": 3,
                "min_age": 18,
                "max_age": 35,
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
                min_age=event["min_age"],
                max_age=event["max_age"],
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
