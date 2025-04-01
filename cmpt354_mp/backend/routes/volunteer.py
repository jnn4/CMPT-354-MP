from flask import Blueprint, request, jsonify
from models import Volunteer, db
from sqlalchemy.exc import IntegrityError
from datetime import date

volunteer_bp = Blueprint('volunteer', __name__, url_prefix='/volunteers')

# Create a new volunteer
@volunteer_bp.route('/', methods=['POST'])
def create_volunteer():
    try:
        data = request.get_json()

        name = data.get('name')
        contact = data.get('contact')
        skills = data.get('skills')
        availability = data.get('availability')

        # Validation
        if not name or not contact:
            return jsonify({"message": "Name and Contact are required!"}), 400

        # Create new volunteer
        new_volunteer = Volunteer(name=name, contact=contact, skills=skills, availability=availability)
        db.session.add(new_volunteer)
        db.session.commit()

        return jsonify({
            "message": "Volunteer created successfully!",
            "volunteer_id": new_volunteer.id,
            "name": new_volunteer.name,
            "contact": new_volunteer.contact,
            "skills": new_volunteer.skills,
            "availability": new_volunteer.availability
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "A database error occurred!"}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# Get volunteer by ID
@volunteer_bp.route('/<int:volunteer_id>', methods=['GET'])
def get_volunteer_by_id(volunteer_id):
    try:
        volunteer = Volunteer.query.get(volunteer_id)
        if not volunteer:
            return jsonify({"message": "Volunteer not found!"}), 404

        return jsonify({
            "volunteer_id": volunteer.id,
            "name": volunteer.name,
            "contact": volunteer.contact,
            "skills": volunteer.skills,
            "availability": volunteer.availability
        }), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Update volunteer details
@volunteer_bp.route('/<int:volunteer_id>', methods=['PUT'])
def update_volunteer(volunteer_id):
    try:
        data = request.get_json()
        volunteer = Volunteer.query.get(volunteer_id)

        if not volunteer:
            return jsonify({"message": "Volunteer not found!"}), 404

        name = data.get('name', volunteer.name)
        contact = data.get('contact', volunteer.contact)
        skills = data.get('skills', volunteer.skills)
        availability = data.get('availability', volunteer.availability)

        # Update volunteer fields
        volunteer.name = name
        volunteer.contact = contact
        volunteer.skills = skills
        volunteer.availability = availability

        db.session.commit()

        return jsonify({
            "message": "Volunteer updated successfully!",
            "volunteer_id": volunteer.id,
            "name": volunteer.name,
            "contact": volunteer.contact,
            "skills": volunteer.skills,
            "availability": volunteer.availability
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# Delete volunteer by ID
@volunteer_bp.route('/<int:volunteer_id>', methods=['DELETE'])
def delete_volunteer(volunteer_id):
    try:
        volunteer = Volunteer.query.get(volunteer_id)

        if not volunteer:
            return jsonify({"message": "Volunteer not found!"}), 404

        db.session.delete(volunteer)
        db.session.commit()

        return jsonify({"message": "Volunteer deleted successfully!"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


# Populate the Volunteer table
@volunteer_bp.route('/populate', methods=['POST'])
def populate_volunteer():
    try:
        volunteer_data = [
            {"volunteer_id": 1, "role": "Event Coordinator", "start_date": date(2025, 1, 10), "end_date": date(2025, 5, 10)},
            {"volunteer_id": 2, "role": "Mentor", "start_date": date(2025, 2, 1), "end_date": date(2025, 6, 1)},
            {"volunteer_id": 3, "role": "Workshop Leader", "start_date": date(2025, 3, 15), "end_date": date(2025, 7, 15)},
            {"volunteer_id": 4, "role": "Event Coordinator", "start_date": date(2025, 4, 1), "end_date": None},  # Ongoing volunteer
            {"volunteer_id": 5, "role": "Admin Assistant", "start_date": date(2025, 1, 20), "end_date": date(2025, 5, 20)},
            {"volunteer_id": 6, "role": "Marketing Assistant", "start_date": date(2025, 2, 10), "end_date": date(2025, 6, 10)},
            {"volunteer_id": 7, "role": "Volunteer Trainer", "start_date": date(2025, 3, 5), "end_date": date(2025, 7, 5)},
            {"volunteer_id": 8, "role": "Event Coordinator", "start_date": date(2025, 4, 10), "end_date": None},  # Ongoing volunteer
            {"volunteer_id": 9, "role": "Workshop Leader", "start_date": date(2025, 5, 1), "end_date": date(2025, 9, 1)},
            {"volunteer_id": 10, "role": "Admin Assistant", "start_date": date(2025, 6, 1), "end_date": date(2025, 10, 1)}
        ]
        
        for volunteer_data in volunteer_data:
            volunteer = Volunteer(**volunteer_data)
            db.session.add(volunteer)

        db.session.commit()
        return jsonify({"message": "Volunteer populated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to populate Volunteer", "error": str(e)}), 500

