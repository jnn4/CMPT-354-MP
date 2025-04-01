from flask import Blueprint, request, jsonify
from models import Audience, db
from sqlalchemy.exc import IntegrityError

audience_bp = Blueprint('audience', __name__, url_prefix='/audience')

# Route to get all audience data
@audience_bp.route('/', methods=['GET'])
def get_all_audiences():
    try:
        audiences = Audience.query.all()

        # Serialize the audience data into a list of dictionaries
        audience_list = [
            {
                'email': audience.email,
                'first_name': audience.first_name,
                'last_name': audience.last_name,
                'age': audience.age,
                'phone_num': audience.phone_num
            }
            for audience in audiences
        ]

        return jsonify({"audiences": audience_list}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to get a specific audience by email
@audience_bp.route('/<string:email>', methods=['GET'])
def get_audience(email):
    try:
        audience = Audience.query.filter_by(email=email).first()

        if not audience:
            return jsonify({"error": "Audience not found!"}), 404

        audience_data = {
            'email': audience.email,
            'first_name': audience.first_name,
            'last_name': audience.last_name,
            'age': audience.age,
            'phone_num': audience.phone_num
        }

        return jsonify({"audience": audience_data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to update a specific audience by email
@audience_bp.route('/<string:email>', methods=['PUT'])
def update_audience(email):
    try:
        audience = Audience.query.filter_by(email=email).first()

        if not audience:
            return jsonify({"error": "Audience not found!"}), 404

        data = request.get_json()

        # Update audience fields
        audience.first_name = data.get('first_name', audience.first_name)
        audience.last_name = data.get('last_name', audience.last_name)
        audience.age = data.get('age', audience.age)
        audience.phone_num = data.get('phone_num', audience.phone_num)

        db.session.commit()

        return jsonify({"message": "Audience updated successfully!"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Route to delete a specific audience by email
@audience_bp.route('/<string:email>', methods=['DELETE'])
def delete_audience(email):
    try:
        audience = Audience.query.filter_by(email=email).first()

        if not audience:
            return jsonify({"error": "Audience not found!"}), 404

        db.session.delete(audience)
        db.session.commit()

        return jsonify({"message": "Audience deleted successfully!"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    

@audience_bp.route('/populate', methods=['POST'])
def populate_audience():
    try:
        audience_data = [
            {"min_age": 18, "max_age": 35, "type": "Young Adults", "event_id": 1},
            {"min_age": 36, "max_age": 50, "type": "Adults", "event_id": 1},
            {"min_age": 51, "max_age": 65, "type": "Middle Aged", "event_id": 2},
            {"min_age": 66, "max_age": 80, "type": "Seniors", "event_id": 2},
            {"min_age": 18, "max_age": 40, "type": "Young Adults", "event_id": 3},
            {"min_age": 25, "max_age": 45, "type": "Professionals", "event_id": 3},
            {"min_age": 5, "max_age": 18, "type": "Teens", "event_id": 4},
            {"min_age": 19, "max_age": 30, "type": "Students", "event_id": 4},
            {"min_age": 30, "max_age": 60, "type": "Working Adults", "event_id": 5},
            {"min_age": 40, "max_age": 65, "type": "Mature Adults", "event_id": 5}
        ]
        
        for audience_data in audience_data:
            audience = Audience(**audience_data)
            db.session.add(audience)

        db.session.commit()
        return jsonify({"message": "Audience populated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to populate Audience", "error": str(e)}), 500
