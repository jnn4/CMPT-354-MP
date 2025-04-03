from flask import Blueprint, request, jsonify
from models import Fines, BorrowTransaction, db

fines_bp = Blueprint('fines', __name__, url_prefix='/fines')

# Create a new fine
@fines_bp.route('/', methods=['POST'])
def create_fine():
    try:
        data = request.get_json()

        # Extract necessary data from the request
        trans_id = data.get('trans_id')
        amount = data.get('amount')

        # Validation
        if not trans_id or not amount:
            return jsonify({"message": "Transaction ID and Amount are required!"}), 400

        transaction = BorrowTransaction.query.get(trans_id)
        if not transaction:
            return jsonify({"message": "Transaction not found!"}), 404

        # Create a new fine
        new_fine = Fines(
            trans_id=trans_id,
            amount=amount
        )

        db.session.add(new_fine)
        db.session.commit()

        return jsonify({
            "message": "Fine created successfully!",
            "fine_id": new_fine.fine_id,
            "trans_id": trans_id,
            "amount": amount
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# Get all fines
@fines_bp.route('/', methods=['GET'])
def get_all_fines():
    try:
        fines = Fines.query.all()
        fines_list = [
            {
                "fine_id": fine.fine_id,
                "trans_id": fine.trans_id,
                "amount": fine.amount,
                "paid": fine.paid,
                "user_id": fine.user_id
            }
            for fine in fines
        ]
        return jsonify(fines_list), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Get a specific fine by ID
@fines_bp.route('/<int:fine_id>', methods=['GET'])
def get_fine_by_id(fine_id):
    fine = Fines.query.get(fine_id)
    if not fine:
        return jsonify({"message": "Fine not found!"}), 404

    return jsonify({
        "fine_id": fine.fine_id,
        "trans_id": fine.trans_id,
        "amount": fine.amount,
        "paid": fine.paid,
        "user_id": fine.user_id
    }), 200

# Update a fine
@fines_bp.route('/<int:fine_id>', methods=['PUT'])
def update_fine(fine_id):
    try:
        fine = Fines.query.get(fine_id)
        if not fine:
            return jsonify({"message": "Fine not found!"}), 404

        data = request.get_json()

        # Update fine details
        amount = data.get('amount', fine.amount)
        paid = data.get('paid', fine.paid)

        fine.amount = amount
        fine.paid = paid
        db.session.commit()

        return jsonify({
            "message": "Fine updated successfully!",
            "fine_id": fine.fine_id,
            "trans_id": fine.trans_id,
            "amount": fine.amount,
            "paid": fine.paid,
            "user_id": fine.user_id
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# Delete a fine by ID
@fines_bp.route('/<int:fine_id>', methods=['DELETE'])
def delete_fine(fine_id):
    fine = Fines.query.get(fine_id)
    if not fine:
        return jsonify({"message": "Fine not found!"}), 404

    try:
        db.session.delete(fine)
        db.session.commit()
        return jsonify({"message": "Fine deleted successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# Populate the table with fines
@fines_bp.route('/populate', methods=['POST'])
def populate_fines():
    try:
        fines_data = [
            {"amount": 15.75, "paid": False, "trans_id": 1, "user_id": 1},
            {"amount": 5.50, "paid": True, "trans_id": 2, "user_id": 2},
            {"amount": 10.00, "paid": False, "trans_id": 3, "user_id": 3},
            {"amount": 20.25, "paid": True, "trans_id": 4, "user_id": 4},
            {"amount": 8.99, "paid": False, "trans_id": 5, "user_id": 5},
            {"amount": 12.00, "paid": False, "trans_id": 6, "user_id": 6},
            {"amount": 25.00, "paid": True, "trans_id": 7, "user_id": 7},
            {"amount": 30.50, "paid": False, "trans_id": 8, "user_id": 8},
            {"amount": 3.75, "paid": True, "trans_id": 9, "user_id": 9},
            {"amount": 18.25, "paid": False, "trans_id": 10, "user_id": 10}
        ]

        for fine_data in fines_data:
            fine = Fines(**fine_data)
            db.session.add(fine)
        
        db.session.commit()
        return jsonify({"message": "Fines populated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to populate Fines", "error": str(e)}), 500
