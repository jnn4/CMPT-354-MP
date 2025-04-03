from flask import Blueprint, request, jsonify
from models import BorrowTransaction, User, Item, db
from datetime import datetime

transactions_bp = Blueprint('transactions', __name__, url_prefix='/transactions')

# Create a new borrow transaction
@transactions_bp.route('/', methods=['POST'])
def create_transaction():
    try:
        data = request.get_json()
        print("Received data:", data)  # Debug log
        
        # Extract necessary data from the request
        user_id = data.get('user_id')
        item_id = data.get('item_id')
        borrowed_at = data.get('borrowed_at')

        # Validation
        if not user_id or not item_id:
            return jsonify({
                "message": "Missing required fields",
                "required": ["user_id", "item_id"],
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

        # Handle borrowed_at date
        try:
            if borrowed_at:
                # If borrowed_at is provided, parse it
                borrowed_at = datetime.fromisoformat(borrowed_at.replace('Z', '+00:00'))
            else:
                # If not provided, use current time
                borrowed_at = datetime.utcnow()
        except ValueError as e:
            return jsonify({"message": f"Invalid borrowed_at date format: {str(e)}"}), 400

        # Create and add the new borrow transaction to the database
        new_transaction = BorrowTransaction(
            user_id=user_id,
            item_id=item_id,
            borrowed_at=borrowed_at
        )

        db.session.add(new_transaction)
        db.session.commit()

        return jsonify({
            "message": "Transaction created successfully!",
            "trans_id": new_transaction.trans_id,
            "user_id": user_id,
            "item_id": item_id,
            "borrowed_at": borrowed_at.strftime('%Y-%m-%d %H:%M:%S') if borrowed_at else None
        }), 201

    except ValueError as e:
        db.session.rollback()
        print("ValueError:", str(e))  # Debug log
        return jsonify({"message": f"Invalid date format: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        print("Exception:", str(e))  # Debug log
        return jsonify({"message": f"Failed to create transaction: {str(e)}"}), 500

# Get all borrow transactions
@transactions_bp.route('/', methods=['GET'])
def get_all_transactions():
    try:
        transactions = BorrowTransaction.query.all()
        transactions_list = [
            {
                "trans_id": trans.trans_id,
                "borrowed_at": trans.borrowed_at.strftime('%Y-%m-%d %H:%M:%S') if trans.borrowed_at else None,
                "returned_at": trans.returned_at.strftime('%Y-%m-%d %H:%M:%S') if trans.returned_at else None,
                "user_id": trans.user_id,
                "item_id": trans.item_id
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
        "borrowed_at": transaction.borrowed_at.strftime('%Y-%m-%d %H:%M:%S') if transaction.borrowed_at else None,
        "returned_at": transaction.returned_at.strftime('%Y-%m-%d %H:%M:%S') if transaction.returned_at else None,
        "user_id": transaction.user_id,
        "item_id": transaction.item_id
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
        borrowed_at = data.get('borrowed_at', transaction.borrowed_at)
        returned_at = data.get('returned_at', transaction.returned_at)

        transaction.borrowed_at = borrowed_at
        transaction.returned_at = returned_at
        db.session.commit()

        return jsonify({
            "message": "Transaction updated successfully!",
            "trans_id": transaction.trans_id,
            "borrowed_at": transaction.borrowed_at.strftime('%Y-%m-%d %H:%M:%S') if transaction.borrowed_at else None,
            "returned_at": transaction.returned_at.strftime('%Y-%m-%d %H:%M:%S') if transaction.returned_at else None
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
            {"trans_id": 1, "user_id": 1, "item_id": 1, "borrowed_at": datetime(2025, 4, 1, 10, 0, 0)},
            {"trans_id": 2, "user_id": 2, "item_id": 2, "borrowed_at": datetime(2025, 4, 2, 11, 30, 0)},
            {"trans_id": 3, "user_id": 3, "item_id": 3, "borrowed_at": datetime(2025, 4, 3, 9, 15, 0)},
            {"trans_id": 4, "user_id": 4, "item_id": 4, "borrowed_at": datetime(2025, 4, 4, 14, 45, 0)},
            {"trans_id": 5, "user_id": 5, "item_id": 5, "borrowed_at": datetime(2025, 4, 5, 13, 0, 0)},
            {"trans_id": 6, "user_id": 6, "item_id": 6, "borrowed_at": datetime(2025, 4, 6, 16, 30, 0)},
            {"trans_id": 7, "user_id": 7, "item_id": 7, "borrowed_at": datetime(2025, 4, 7, 10, 0, 0)},
            {"trans_id": 8, "user_id": 8, "item_id": 8, "borrowed_at": datetime(2025, 4, 8, 17, 15, 0)},
            {"trans_id": 9, "user_id": 9, "item_id": 9, "borrowed_at": datetime(2025, 4, 9, 11, 30, 0)},
            {"trans_id": 10, "user_id": 10, "item_id": 10, "borrowed_at": datetime(2025, 4, 10, 14, 45, 0)}
        ]

        inserted_count = 0
        skipped_count = 0

        for trans_data in transaction_data:
            # Check if transaction already exists
            existing_transaction = BorrowTransaction.query.filter_by(trans_id=trans_data["trans_id"]).first()
            
            if not existing_transaction:
                # Check if user exists
                user = User.query.get(trans_data["user_id"])
                if not user:
                    print(f"Skipping transaction {trans_data['trans_id']}: User {trans_data['user_id']} does not exist")
                    skipped_count += 1
                    continue

                # Check if item exists
                item = Item.query.get(trans_data["item_id"])
                if not item:
                    print(f"Skipping transaction {trans_data['trans_id']}: Item {trans_data['item_id']} does not exist")
                    skipped_count += 1
                    continue

                transaction = BorrowTransaction(**trans_data)
                db.session.add(transaction)
                inserted_count += 1
            else:
                skipped_count += 1

        db.session.commit()
        return jsonify({
            "message": "Transaction population completed",
            "inserted": inserted_count,
            "skipped": skipped_count
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to populate transaction", "error": str(e)}), 500
