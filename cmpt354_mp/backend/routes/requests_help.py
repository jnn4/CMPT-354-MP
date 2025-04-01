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
    
@requests_help_bp.route('/populate', methods=['POST'])
def populate_requests_help():
    try:
        request_help_data = [
            {"request_help_id": 1, "request_text": "I need help with accessing my account.", "response_text": "Please try resetting your password.", "status": "resolved", "user_id": 1, "staff_id": 1},
            {"request_help_id": 2, "request_text": "I am having trouble with the booking system.", "response_text": "Can you provide more details about the issue?", "status": "in progress", "user_id": 2, "staff_id": 2},
            {"request_help_id": 3, "request_text": "Can someone help me with an error while logging in?", "response_text": "We are looking into the issue.", "status": "in progress", "user_id": 3, "staff_id": 3},
            {"request_help_id": 4, "request_text": "How do I update my account details?", "response_text": "You can update your account details from the profile section.", "status": "resolved", "user_id": 4, "staff_id": 4},
            {"request_help_id": 5, "request_text": "I need assistance with resetting my password.", "response_text": "Please follow the instructions sent to your email.", "status": "resolved", "user_id": 5, "staff_id": 5},
            {"request_help_id": 6, "request_text": "I'm facing an issue with the search feature.", "response_text": "We have escalated the issue to the technical team.", "status": "in progress", "user_id": 6, "staff_id": 6},
            {"request_help_id": 7, "request_text": "Can I change my reservation?", "response_text": "Yes, you can update your reservation through the website.", "status": "resolved", "user_id": 7, "staff_id": 7},
            {"request_help_id": 8, "request_text": "I need help understanding the billing system.", "response_text": "I can walk you through the process in a call.", "status": "resolved", "user_id": 8, "staff_id": 8},
            {"request_help_id": 9, "request_text": "I am unable to access my account on mobile.", "response_text": "Try clearing the cache and cookies, and try again.", "status": "resolved", "user_id": 9, "staff_id": 9},
            {"request_help_id": 10, "request_text": "Could you help me with the refund process?", "response_text": "Please follow the refund guidelines provided in your email.", "status": "resolved", "user_id": 10, "staff_id": 10}
        ]

        for request_help_data in request_help_data:
            request_help = RequestHelp(**request_help_data)
            db.session.add(request_help)

        db.session.commit()
        return jsonify({"message": "Items populated successfully"}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to populate Items", "error": str(e)}), 500


