from flask import Blueprint, request, jsonify
from models import Item, User, BorrowTransaction, Fine
from extensions import db
from flask_cors import CORS
from datetime import datetime, timedelta

# Create Blueprint for authentication routes
items_bp = Blueprint('item', __name__)

# Enable CORS for all routes in the Blueprint
CORS(items_bp, resources={r"/*": {"origins": "http://localhost:5173"}})

# Get all items
@items_bp.route('/', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([
        {
            "item_id": item.item_id,
            "title": item.title,
            "author": item.author,
            "pub_year": item.pub_year,
            "status": item.status,
            "type": item.type
        } for item in items
    ])

# Borrow an item
@items_bp.route('/borrow', methods=['POST'])
def borrow_item():
    data = request.json
    print("Received data:", data)  # Log incoming request data

    # Extract fields
    item_id = data.get('item_id')
    user_email = data.get('user_email')

    # Log extracted fields
    print(f"item_id: {item_id}, user_email: {user_email}")

    # Query for item and user
    item = Item.query.get(item_id)
    user = User.query.filter_by(email=user_email).first()

    # Log query results
    print("Queried Item:", item)
    print("Queried User:", user)

    if not item or not user:
        return jsonify({"message": "Item or user not found"}), 404

    if item.status != 'available':
        return jsonify({"message": "Item not available"}), 400

    try:
        new_transaction = BorrowTransaction(
            user_email=user_email,
            item_id=item_id,
            borrow_date=datetime.utcnow(),
            due_date=datetime.utcnow() + timedelta(days=14)
        )
        db.session.add(new_transaction)
        item.status = 'borrowed'
        db.session.commit()

        return jsonify({
            "message": "Item borrowed successfully",
            "item": {
                "item_id": item.item_id,
                "title": item.title,
                "type": item.type.lower(),
                "status": item.status
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error during borrowing: {e}")  # Log exception details
        return jsonify({"message": str(e)}), 500

@items_bp.route('/borrow', methods=['OPTIONS'])
def handle_options():
    return '', 200


# Return an item
@items_bp.route('/return', methods=['POST'])
def return_item():
    data = request.json
    transaction = BorrowTransaction.query.filter_by(
        item_id=data['item_id'],
        user_email=data['user_email'],
        return_date=None
    ).first()

    if not transaction:
        return jsonify({'message': 'No active borrowing record found'}), 404

    try:
        # Update transaction
        transaction.return_date = datetime.utcnow()
        
        # Update item status
        transaction.item.status = 'available'
        db.session.commit()
        
        return jsonify({
            'message': 'Item returned successfully',
            'item': {
                'item_id': transaction.item.item_id,
                'title': transaction.item.title,
                'author': transaction.item.author,
                'type': transaction.item.type,
                'status': transaction.item.status
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

