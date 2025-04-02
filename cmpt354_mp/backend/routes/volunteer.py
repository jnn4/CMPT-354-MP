from flask import Blueprint, request, jsonify
from extensions import db
from flask_cors import CORS  # Ensure CORS is imported
from models import Person, User, Staff, Volunteer
from datetime import datetime

# Create Blueprint for authentication routes
volunteer_bp = Blueprint('volunteer', __name__)

# Enable CORS for all routes in the Blueprint
CORS(volunteer_bp, resources={r"/*": {"origins": "http://localhost:5173"}})

# Start volunteering
@volunteer_bp.route('/start', methods=['POST'])
def start_volunteering():
    data = request.json
    email = data.get('email')
    
    if not email:
        return jsonify({'message': 'Email required'}), 400

    try:
        # Check for existing active volunteering
        active_volunteer = Volunteer.query.filter_by(email=email, end_date=None).first()
        if active_volunteer:
            return jsonify({'message': 'Already volunteering'}), 400

        # Create new volunteer entry
        new_volunteer = Volunteer(
            email=email,
            start_date=datetime.utcnow().date(),
            end_date=None
        )
        db.session.add(new_volunteer)
        db.session.commit()
        
        return jsonify({
            'message': 'Volunteering started successfully',
            'volunteer': {
                'start_date': new_volunteer.start_date.isoformat(),
                'end_date': None
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

# Stop volunteering
@volunteer_bp.route('/stop', methods=['POST'])
def stop_volunteering():
    data = request.json
    email = data.get('email')
    
    if not email:
        return jsonify({'message': 'Email required'}), 400

    try:
        volunteer = Volunteer.query.filter_by(email=email, end_date=None).first()
        if not volunteer:
            return jsonify({'message': 'No active volunteering'}), 404

        volunteer.end_date = datetime.utcnow().date()
        db.session.commit()
        
        return jsonify({
            'message': 'Volunteering stopped successfully',
            'volunteer': {
                'start_date': volunteer.start_date.isoformat(),
                'end_date': volunteer.end_date.isoformat()
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500
