from flask import Blueprint, request, jsonify
from models import RequestHelp, db

requests_help_bp = Blueprint('requests_help', __name__, url_prefix='/requests_help')

# Create a new help request
@requests_help_bp.route('create', methods=['POST'])
def submit_help_request():
    data = request.json
    user_email = data.get('user_email')
    request_text = data.get('request_text')

    if not user_email or not request_text:
        return jsonify({'message': 'Missing required fields'}), 400

    try:
        new_request = RequestHelp(
            user_email=user_email,
            request_text=request_text,
            status=True  # Default to open
        )
        db.session.add(new_request)
        db.session.commit()
        return jsonify({'message': 'Help request submitted successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# === Get all help Request ====
@requests_help_bp.route('/', methods=['GET'])
def get_all_help_requests():
    help_requests = RequestHelp.query.all()

    return jsonify([{
        'request_id': req.request_id,
        'user_email': req.user_email,
        'request_text': req.request_text,
        'status': 'Open' if req.status else 'Closed',
        'created_at': req.created_at.isoformat()
    } for req in help_requests]), 200

        
# Update reuqest
@requests_help_bp.route('/update/<int:request_id>', methods=['PATCH'])
def update_help_request_status(request_id):
    data = request.json
    new_status = data.get('status')  # Boolean: True for open, False for closed

    if new_status is None:
        return jsonify({'message': 'Missing required field: status'}), 400

    try:
        help_request = RequestHelp.query.get(request_id)
        if not help_request:
            return jsonify({'message': 'Help request not found'}), 404

        help_request.status = new_status
        db.session.commit()
        return jsonify({'message': 'Help request status updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500