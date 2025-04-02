from flask import Blueprint, request, jsonify
from extensions import db
from models import Staff
from werkzeug.security import generate_password_hash


# staff_bp = Blueprint('staff', __name__, url_prefix='/staff')

# Get all staff members
@staff_bp.route('/staff/', methods=['GET'])
def get_all_staff():
    staff = Staff.query.all()
    return jsonify([{
        'staff_id': s.staff_id,
        'email': s.email,
        'position': s.position,
        'wage': s.wage
    } for s in staff]), 200

# Get a specific staff member by ID
@staff_bp.route('/staff/<int:staff_id>', methods=['GET'])
def get_staff(staff_id):
    staff = Staff.query.get(staff_id)
    if not staff:
        return jsonify({'error': 'Staff member not found'}), 404
    return jsonify({
        'staff_id': staff.staff_id,
        'email': staff.email,
        'position': staff.position,
        'wage': staff.wage
    }), 200

# Create a new staff member
@staff_bp.route('/staff/', methods=['POST'])
def create_staff():
    data = request.json
    if not all(k in data for k in ('email', 'position', 'wage')):
        return jsonify({'error': 'Missing required fields'}), 400
    
#     new_staff = Staff(
#         email=data['email'],
#         position=data['position'],
#         wage=data['wage']
#     )
#     db.session.add(new_staff)
#     db.session.commit()
#     return jsonify({'message': 'Staff member created successfully'}), 201

# Update a staff member
@staff_bp.route('/staff/<int:staff_id>', methods=['PUT'])
def update_staff(staff_id):
    staff = Staff.query.get(staff_id)
    if not staff:
        return jsonify({'error': 'Staff member not found'}), 404
    
#     data = request.json
#     staff.position = data.get('position', staff.position)
#     staff.wage = data.get('wage', staff.wage)
    
#     db.session.commit()
#     return jsonify({'message': 'Staff member updated successfully'}), 200

# Delete a staff member
@staff_bp.route('/staff/<int:staff_id>', methods=['DELETE'])
def delete_staff(staff_id):
    staff = Staff.query.get(staff_id)
    if not staff:
        return jsonify({'error': 'Staff member not found'}), 404
    
    db.session.delete(staff)
    db.session.commit()
    return jsonify({'message': 'Staff member deleted successfully'}), 200

# Populate staff member table
@staff_bp.route("/staff/populate_staff", methods=['POST'])
def populate_staff():
    try:
        staff_data = [
            {"email": "alice@company.com", "position": "Manager", "wage": 60000, "password": generate_password_hash("password1")},
            {"email": "bob@company.com", "position": "Cashier", "wage": 40000, "password": generate_password_hash("password2")},
            {"email": "carol@company.com", "position": "Sales Associate", "wage": 35000, "password": generate_password_hash("password3")},
            {"email": "david@company.com", "position": "Supervisor", "wage": 50000, "password": generate_password_hash("password4")},
            {"email": "eve@company.com", "position": "Customer Service", "wage": 45000, "password": generate_password_hash("password5")},
            {"email": "frank@company.com", "position": "Cashier", "wage": 38000, "password": generate_password_hash("password6")},
            {"email": "grace@company.com", "position": "Security", "wage": 42000, "password": generate_password_hash("password7")},
            {"email": "hank@company.com", "position": "Technician", "wage": 55000, "password": generate_password_hash("password8")},
            {"email": "ivy@company.com", "position": "Marketing", "wage": 65000, "password": generate_password_hash("password9")},
            {"email": "jack@company.com", "position": "HR", "wage": 48000, "password": generate_password_hash("password10")}
        ]

        for staff_data in staff_data:
            staff = Staff(**staff_data)
            db.session.add(staff)

        db.session.commit();
        return jsonify({"message": "Staff populated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to popualte staff", "error": str(e)}), 500
