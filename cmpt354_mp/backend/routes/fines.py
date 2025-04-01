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
        fine_amount = data.get('fine_amount')

        # Validation
        if not trans_id or not fine_amount:
            return jsonify({"message": "Transaction ID and Fine Amount are required!"}), 400

        transaction = BorrowTransaction.query.get(trans_id)
        if not transaction:
            return jsonify({"message": "Transaction not found!"}), 404

        # Create a new fine
        new_fine = Fine(
            trans_id=trans_id,
            fine_amount=fine_amount
        )

        db.session.add(new_fine)
        db.session.commit()

        return jsonify({
            "message": "Fine created successfully!",
            "fine_id": new_fine.fine_id,
            "trans_id": trans_id,
            "fine_amount": fine_amount
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# Get all fines
@fines_bp.route('/', methods=['GET'])
def get_all_fines():
    try:
        fines = Fine.query.all()
        fines_list = [
            {
                "fine_id": fine.fine_id,
                "trans_id": fine.trans_id,
                "fine_amount": fine.fine_amount
            }
            for fine in fines
        ]
        return jsonify(fines_list), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Get a specific fine by ID
@fines_bp.route('/<int:fine_id>', methods=['GET'])
def get_fine_by_id(fine_id):
    fine = Fine.query.get(fine_id)
    if not fine:
        return jsonify({"message": "Fine not found!"}), 404

    return jsonify({
        "fine_id": fine.fine_id,
        "trans_id": fine.trans_id,
        "fine_amount": fine.fine_amount
    }), 200

# Update a fine
@fines_bp.route('/<int:fine_id>', methods=['PUT'])
def update_fine(fine_id):
    try:
        fine = Fine.query.get(fine_id)
        if not fine:
            return jsonify({"message": "Fine not found!"}), 404

        data = request.get_json()

        # Update fine details
        fine_amount = data.get('fine_amount', fine.fine_amount)

        fine.fine_amount = fine_amount
        db.session.commit()

        return jsonify({
            "message": "Fine updated successfully!",
            "fine_id": fine.fine_id,
            "trans_id": fine.trans_id,
            "fine_amount": fine.fine_amount
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# Delete a fine by ID
@fines_bp.route('/<int:fine_id>', methods=['DELETE'])
def delete_fine(fine_id):
    fine = Fine.query.get(fine_id)
    if not fine:
        return jsonify({"message": "Fine not found!"}), 404

    try:
        db.session.delete(fine)
        db.session.commit()
        return jsonify({"message": "Fine deleted successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500
