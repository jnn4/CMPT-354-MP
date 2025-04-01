from flask import Blueprint, request, jsonify
from extensions import db
from models import Event

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
