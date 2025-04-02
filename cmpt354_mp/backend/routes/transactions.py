from flask import Blueprint, request, jsonify
from models import BorrowTransaction, User, Item, db
from datetime import datetime

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
        return_date = data.get('return_date')

        # Validation
        if not user_id or not item_id or not borrow_date or not due_date:
            return jsonify({
                "message": "Missing required fields",
                "required": ["user_id", "item_id", "borrow_date", "due_date"],
                "received": data
            }), 400

        # Check if user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": f"User with ID {user_id} not found"}), 404

        # Check if item exists
        item = Item.query.get(item_id)
        if not item:
            return jsonify({"message": f"Item with ID {item_id} not found"}), 404

        # Check if item is already borrowed
        if item.status == "borrowed":
            return jsonify({"message": "Item is already borrowed"}), 400

        # Create and add the new borrow transaction to the database
        new_transaction = BorrowTransaction(
            user_id=user_id,
            item_id=item_id,
            borrow_date=datetime.fromisoformat(borrow_date.replace('Z', '+00:00')),
            due_date=datetime.fromisoformat(due_date.replace('Z', '+00:00')),
            return_date=datetime.fromisoformat(return_date.replace('Z', '+00:00')) if return_date else None
        )

        db.session.add(new_transaction)
        db.session.commit()

        return jsonify({
            "message": "Transaction created successfully!",
            "trans_id": new_transaction.trans_id,
            "user_id": user_id,
            "item_id": item_id,
            "borrow_date": borrow_date,
            "due_date": due_date,
            "return_date": return_date
        }), 201

    except ValueError as e:
        db.session.rollback()
        return jsonify({"message": f"Invalid date format: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Failed to create transaction: {str(e)}"}), 500

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
    
# Populate the transaction table
@transactions_bp.route('/populate', methods=['POST'])
def populate_transactions():
    try:
        transaction_data = [
            {"id": 1, "user_id": 1, "book_id": 1, "borrowed_at": datetime(2025, 4, 1, 10, 0, 0)},
            {"id": 2, "user_id": 2, "book_id": 2, "borrowed_at": datetime(2025, 4, 2, 11, 30, 0)},
            {"id": 3, "user_id": 3, "book_id": 3, "borrowed_at": datetime(2025, 4, 3, 9, 15, 0)},
            {"id": 4, "user_id": 4, "book_id": 4, "borrowed_at": datetime(2025, 4, 4, 14, 45, 0)},
            {"id": 5, "user_id": 5, "book_id": 5, "borrowed_at": datetime(2025, 4, 5, 13, 0, 0)},
            {"id": 6, "user_id": 6, "book_id": 6, "borrowed_at": datetime(2025, 4, 6, 16, 30, 0)},
            {"id": 7, "user_id": 7, "book_id": 7, "borrowed_at": datetime(2025, 4, 7, 10, 0, 0)},
            {"id": 8, "user_id": 8, "book_id": 8, "borrowed_at": datetime(2025, 4, 8, 17, 15, 0)},
            {"id": 9, "user_id": 9, "book_id": 9, "borrowed_at": datetime(2025, 4, 9, 11, 30, 0)},
            {"id": 10, "user_id": 10, "book_id": 10, "borrowed_at": datetime(2025, 4, 10, 14, 45, 0)}
        ]

        for transaction_data in transaction_data:
            transaction = BorrowTransaction(**transaction_data)
            db.session.add(transaction)

        db.session.commit()
        return jsonify({"message": "Transaction populated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to populate transaction", "error": str(e)}), 500
