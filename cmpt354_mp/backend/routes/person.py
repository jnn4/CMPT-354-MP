from flask import Blueprint, request, jsonify
from models import Person, db
from sqlalchemy.exc import IntegrityError

person_bp = Blueprint('person', __name__, url_prefix='/persons')

# Create a new person
@person_bp.route('/', methods=['POST'])
def create_person():
    try:
        data = request.get_json()

        name = data.get('name')
        contact = data.get('contact')
        address = data.get('address')

        # Validation
        if not name or not contact:
            return jsonify({"message": "Name and Contact are required!"}), 400

        # Create new person
        new_person = Person(name=name, contact=contact, address=address)
        db.session.add(new_person)
        db.session.commit()

        return jsonify({
            "message": "Person created successfully!",
            "person_id": new_person.id,
            "name": new_person.name,
            "contact": new_person.contact,
            "address": new_person.address
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "A database error occurred!"}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# Get person by ID
@person_bp.route('/<int:person_id>', methods=['GET'])
def get_person_by_id(person_id):
    try:
        person = Person.query.get(person_id)
        if not person:
            return jsonify({"message": "Person not found!"}), 404

        return jsonify({
            "person_id": person.id,
            "name": person.name,
            "contact": person.contact,
            "address": person.address
        }), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Update person details
@person_bp.route('/<int:person_id>', methods=['PUT'])
def update_person(person_id):
    try:
        data = request.get_json()
        person = Person.query.get(person_id)

        if not person:
            return jsonify({"message": "Person not found!"}), 404

        name = data.get('name', person.name)
        contact = data.get('contact', person.contact)
        address = data.get('address', person.address)

        # Update person fields
        person.name = name
        person.contact = contact
        person.address = address

        db.session.commit()

        return jsonify({
            "message": "Person updated successfully!",
            "person_id": person.id,
            "name": person.name,
            "contact": person.contact,
            "address": person.address
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# Delete person by ID
@person_bp.route('/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
    try:
        person = Person.query.get(person_id)

        if not person:
            return jsonify({"message": "Person not found!"}), 404

        db.session.delete(person)
        db.session.commit()

        return jsonify({"message": "Person deleted successfully!"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500
