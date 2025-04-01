from flask import Blueprint, request, jsonify
from models import RequestHelp, db

requests_help_bp = Blueprint('requests_help', __name__, url_prefix='/requests_help')

# Create a new help request
@requests_help_bp.route('/', methods=['POST'])
def create_request_help():
    try:
        data = request.get_json()

        # Extract necessary data from the request
        user_id = data.get('user_id')
        staff_id = data.get('staff_id')
        request_text = data.get('request_text')
        status = data.get('status')

        # Validation
        if not user_id or not staff_id or not request_text or not status:
            return jsonify({"message": "User ID, Staff ID, Request Text, and Status are required!"}), 400

        # Create a new help request
        new_request = RequestHelp(
            user_id=user_id,
            staff_id=staff_id,
            request_text=request_text,
            status=status
        )

        db.session.add(new_request)
        db.session.commit()

        return jsonify({
            "message": "Help request created successfully!",
            "request_id": new_request.request_help_id,
            "user_id": user_id,
            "staff_id": staff_id,
            "request_text": request_text,
            "status": status
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# Get all help requests
@requests_help_bp.route('/', methods=['GET'])
def get_all_requests_help():
    try:
        requests = RequestHelp.query.all()
        requests_list = [
            {
                "request_help_id": request.request_help_id,
                "user_id": request.user_id,
                "staff_id": request.staff_id,
                "request_text": request.request_text,
                "response_text": request.response_text,
                "status": request.status
            }
            for request in requests
        ]
        return jsonify(requests_list), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Get a specific help request by ID
@requests_help_bp.route('/<int:request_help_id>', methods=['GET'])
def get_request_help_by_id(request_help_id):
    request_help = RequestHelp.query.get(request_help_id)
    if not request_help:
        return jsonify({"message": "Request not found!"}), 404

    return jsonify({
        "request_help_id": request_help.request_help_id,
        "user_id": request_help.user_id,
        "staff_id": request_help.staff_id,
        "request_text": request_help.request_text,
        "response_text": request_help.response_text,
        "status": request_help.status
    }), 200

# Update a help request (e.g., status or response text)
@requests_help_bp.route('/<int:request_help_id>', methods=['PUT'])
def update_request_help(request_help_id):
    try:
        data = request.get_json()
        request_help = RequestHelp.query.get(request_help_id)

        if not request_help:
            return jsonify({"message": "Request not found!"}), 404

        # Update the help request fields
        request_help.status = data.get('status', request_help.status)
        request_help.response_text = data.get('response_text', request_help.response_text)

        db.session.commit()

        return jsonify({
            "message": "Help request updated successfully!",
            "request_help_id": request_help.request_help_id,
            "status": request_help.status,
            "response_text": request_help.response_text
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# Delete a help request by ID
@requests_help_bp.route('/<int:request_help_id>', methods=['DELETE'])
def delete_request_help(request_help_id):
    try:
        request_help = RequestHelp.query.get(request_help_id)

        if not request_help:
            return jsonify({"message": "Request not found!"}), 404

        db.session.delete(request_help)
        db.session.commit()

        return jsonify({"message": "Help request deleted successfully!"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500
