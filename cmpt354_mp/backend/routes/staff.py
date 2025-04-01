# from flask import Blueprint, request, jsonify
# from extensions import db
# from models import Staff

# staff_bp = Blueprint('staff', __name__, url_prefix='/staff')

# # Get all staff members
# @staff_bp.route('/', methods=['GET'])
# def get_all_staff():
#     staff = Staff.query.all()
#     return jsonify([{
#         'staff_id': s.staff_id,
#         'email': s.email,
#         'position': s.position,
#         'wage': s.wage
#     } for s in staff]), 200

# # Get a specific staff member by ID
# @staff_bp.route('/<int:staff_id>', methods=['GET'])
# def get_staff(staff_id):
#     staff = Staff.query.get(staff_id)
#     if not staff:
#         return jsonify({'error': 'Staff member not found'}), 404
#     return jsonify({
#         'staff_id': staff.staff_id,
#         'email': staff.email,
#         'position': staff.position,
#         'wage': staff.wage
#     }), 200

# # Create a new staff member
# @staff_bp.route('/', methods=['POST'])
# def create_staff():
#     data = request.json
#     if not all(k in data for k in ('email', 'position', 'wage')):
#         return jsonify({'error': 'Missing required fields'}), 400
    
#     new_staff = Staff(
#         email=data['email'],
#         position=data['position'],
#         wage=data['wage']
#     )
#     db.session.add(new_staff)
#     db.session.commit()
#     return jsonify({'message': 'Staff member created successfully'}), 201

# # Update a staff member
# @staff_bp.route('/<int:staff_id>', methods=['PUT'])
# def update_staff(staff_id):
#     staff = Staff.query.get(staff_id)
#     if not staff:
#         return jsonify({'error': 'Staff member not found'}), 404
    
#     data = request.json
#     staff.position = data.get('position', staff.position)
#     staff.wage = data.get('wage', staff.wage)
    
#     db.session.commit()
#     return jsonify({'message': 'Staff member updated successfully'}), 200

# # Delete a staff member
# @staff_bp.route('/<int:staff_id>', methods=['DELETE'])
# def delete_staff(staff_id):
#     staff = Staff.query.get(staff_id)
#     if not staff:
#         return jsonify({'error': 'Staff member not found'}), 404
    
#     db.session.delete(staff)
#     db.session.commit()
#     return jsonify({'message': 'Staff member deleted successfully'}), 200
