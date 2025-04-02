from flask import Blueprint, request, jsonify
from models import Person, db
from sqlalchemy.exc import IntegrityError
from datetime import date

person_bp = Blueprint('person', __name__)

# Get all people
@person_bp.route('/', methods=['GET'])
def get_persons(): 
    person = Person.query.all()
    persons_data = [
        {
            "email": person.email,
            "firstName": person.first_name,
            "lastName": person.last_name,
            "phoneNum": person.phone_num,
            "age": person.age
        }
        for person in person
    ]
    return jsonify(persons_data), 200


# Create a new person
@person_bp.route('/post', methods=['POST'])
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

# Populate the persons table
@person_bp.route('/populate', methods=['POST'])
def populate_persons():
    try:
        person_data = [
            {"email": "alice@example.com", "first_name": "Alice", "last_name": "Johnson", "phone_num": "123-456-7890", "age": 28},
            {"email": "bob@example.com", "first_name": "Bob", "last_name": "Smith", "phone_num": "234-567-8901", "age": 35},
            {"email": "charlie@example.com", "first_name": "Charlie", "last_name": "Brown", "phone_num": "345-678-9012", "age": 40},
            {"email": "dave@example.com", "first_name": "Dave", "last_name": "Williams", "phone_num": "456-789-0123", "age": 29},
            {"email": "eve@example.com", "first_name": "Eve", "last_name": "Davis", "phone_num": "567-890-1234", "age": 26},
            {"email": "frank@example.com", "first_name": "Frank", "last_name": "Miller", "phone_num": "678-901-2345", "age": 32},
            {"email": "grace@example.com", "first_name": "Grace", "last_name": "Taylor", "phone_num": "789-012-3456", "age": 38},
            {"email": "heidi@example.com", "first_name": "Heidi", "last_name": "Anderson", "phone_num": "890-123-4567", "age": 31},
            {"email": "ivan@example.com", "first_name": "Ivan", "last_name": "Moore", "phone_num": "901-234-5678", "age": 27},
            {"email": "judy@example.com", "first_name": "Judy", "last_name": "Martinez", "phone_num": "012-345-6789", "age": 33},
            {"email": "alice@company.com", "first_name": "Alice", "last_name": "Johnson", "phone_num": "123-456-7890", "age": 28},
            {"email": "bob@company.com", "first_name": "Bob", "last_name": "Smith", "phone_num": "234-567-8901", "age": 35},
            {"email": "carol@company.com", "first_name": "Carol", "last_name": "Williams", "phone_num": "345-678-9012", "age": 39},
            {"email": "david@company.com", "first_name": "David", "last_name": "Taylor", "phone_num": "456-789-0123", "age": 45},
            {"email": "eve@company.com", "first_name": "Eve", "last_name": "Johnson", "phone_num": "567-890-1234", "age": 41},
            {"email": "frank@company.com", "first_name": "Frank", "last_name": "Davis", "phone_num": "678-901-2345", "age": 37},
            {"email": "grace@company.com", "first_name": "Grace", "last_name": "Miller", "phone_num": "789-012-3456", "age": 29},
            {"email": "hank@company.com", "first_name": "Hank", "last_name": "Wilson", "phone_num": "890-123-4567", "age": 42},
            {"email": "ivy@company.com", "first_name": "Ivy", "last_name": "Moore", "phone_num": "901-234-5678", "age": 25},
            {"email": "jack@company.com", "first_name": "Jack", "last_name": "Martinez", "phone_num": "012-345-6789", "age": 32}
        ]
        for person_data in person_data:
            person = Person(**person_data)
            db.session.add(person)

        db.session.commit()
        return jsonify({"message": "Volunteer person successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to person Volunteer", "error": str(e)}), 500