from flask import Blueprint, request, jsonify
from models import Room, db

rooms_bp = Blueprint('rooms', __name__, url_prefix='/rooms')

# Create a new room
@rooms_bp.route('/', methods=['POST'])
def create_room():
    try:
        data = request.get_json()

        # Extract the necessary data from the request
        name = data.get('name')
        capacity = data.get('capacity')

        if not name or not capacity:
            return jsonify({"message": "Name and capacity are required!"}), 400

        # Create and add the new room to the database
        new_room = Room(name=name, capacity=capacity)
        db.session.add(new_room)
        db.session.commit()

        return jsonify({
            "message": "Room created successfully!",
            "room_id": new_room.room_id,
            "name": new_room.name,
            "capacity": new_room.capacity
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# Get all rooms
@rooms_bp.route('/', methods=['GET'])
def get_all_rooms():
    try:
        rooms = Room.query.all()
        rooms_list = [
            {"room_id": room.room_id, "name": room.name, "capacity": room.capacity}
            for room in rooms
        ]
        return jsonify(rooms_list), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Get a specific room by ID
@rooms_bp.route('/<int:room_id>', methods=['GET'])
def get_room_by_id(room_id):
    room = Room.query.get(room_id)
    if not room:
        return jsonify({"message": "Room not found!"}), 404

    return jsonify({
        "room_id": room.room_id,
        "name": room.name,
        "capacity": room.capacity
    }), 200

# Update a room's details
@rooms_bp.route('/<int:room_id>', methods=['PUT'])
def update_room(room_id):
    try:
        room = Room.query.get(room_id)
        if not room:
            return jsonify({"message": "Room not found!"}), 404

        data = request.get_json()

        # Update room details
        name = data.get('name', room.name)
        capacity = data.get('capacity', room.capacity)

        room.name = name
        room.capacity = capacity
        db.session.commit()

        return jsonify({
            "message": "Room updated successfully!",
            "room_id": room.room_id,
            "name": room.name,
            "capacity": room.capacity
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# Delete a room by ID
@rooms_bp.route('/<int:room_id>', methods=['DELETE'])
def delete_room(room_id):
    room = Room.query.get(room_id)
    if not room:
        return jsonify({"message": "Room not found!"}), 404

    try:
        db.session.delete(room)
        db.session.commit()
        return jsonify({"message": "Room deleted successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500
