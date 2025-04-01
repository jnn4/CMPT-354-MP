from flask import Blueprint, request, jsonify
from models import BorrowTransaction, User, Item, db

transactions_bp = Blueprint('transactions', __name__, url_prefix='/transactions')

# Create a new borrow transaction
@transactions_bp.route('/', methods=['POST'])
def create_transaction():
    try:
        data = request.get_json()

        # Extract necessary data from the request
        user_id = data.get('user_id')
        item_id = data.get('item_id')
        borrow_date = data.get('borrow_date')
        due_date = data.get('due_date')

        # Validation
        if not user_id or not item_id or not borrow_date or not due_date:
            return jsonify({"message": "User ID, Item ID, Borrow Date, and Due Date are required!"}), 400

        user = User.query.get(user_id)
        item = Item.query.get(item_id)

        if not user or not item:
            return jsonify({"message": "User or Item not found!"}), 404

        # Create and add the new borrow transaction to the database
        new_transaction = BorrowTransaction(
            borrow_date=borrow_date,
            due_date=due_date,
            user_id=user_id
        )

        db.session.add(new_transaction)
        db.session.commit()

        return jsonify({
            "message": "Transaction created successfully!",
            "trans_id": new_transaction.trans_id,
            "user_id": user_id,
            "item_id": item_id,
            "borrow_date": borrow_date,
            "due_date": due_date
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# Get all borrow transactions
@transactions_bp.route('/', methods=['GET'])
def get_all_transactions():
    try:
        transactions = BorrowTransaction.query.all()
        transactions_list = [
            {
                "trans_id": trans.trans_id,
                "borrow_date": trans.borrow_date,
                "due_date": trans.due_date,
                "return_date": trans.return_date,
                "user_id": trans.user_id
            }
            for trans in transactions
        ]
        return jsonify(transactions_list), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Get a specific borrow transaction by ID
@transactions_bp.route('/<int:trans_id>', methods=['GET'])
def get_transaction_by_id(trans_id):
    transaction = BorrowTransaction.query.get(trans_id)
    if not transaction:
        return jsonify({"message": "Transaction not found!"}), 404

    return jsonify({
        "trans_id": transaction.trans_id,
        "borrow_date": transaction.borrow_date,
        "due_date": transaction.due_date,
        "return_date": transaction.return_date,
        "user_id": transaction.user_id
    }), 200

# Update a borrow transaction
@transactions_bp.route('/<int:trans_id>', methods=['PUT'])
def update_transaction(trans_id):
    try:
        transaction = BorrowTransaction.query.get(trans_id)
        if not transaction:
            return jsonify({"message": "Transaction not found!"}), 404

        data = request.get_json()

        # Update transaction details
        borrow_date = data.get('borrow_date', transaction.borrow_date)
        due_date = data.get('due_date', transaction.due_date)
        return_date = data.get('return_date', transaction.return_date)

        transaction.borrow_date = borrow_date
        transaction.due_date = due_date
        transaction.return_date = return_date
        db.session.commit()

        return jsonify({
            "message": "Transaction updated successfully!",
            "trans_id": transaction.trans_id,
            "borrow_date": transaction.borrow_date,
            "due_date": transaction.due_date,
            "return_date": transaction.return_date
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# Delete a borrow transaction by ID
@transactions_bp.route('/<int:trans_id>', methods=['DELETE'])
def delete_transaction(trans_id):
    transaction = BorrowTransaction.query.get(trans_id)
    if not transaction:
        return jsonify({"message": "Transaction not found!"}), 404

    try:
        db.session.delete(transaction)
        db.session.commit()
        return jsonify({"message": "Transaction deleted successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500
