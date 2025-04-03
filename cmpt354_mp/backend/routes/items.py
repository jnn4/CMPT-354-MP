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


def _build_cors_preflight_response():
    response = jsonify({'message': 'CORS preflight'})
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "DELETE, OPTIONS")
    return response

# delete item
@items_bp.route('/delete/<int:item_id>', methods=['DELETE', 'OPTIONS'])
def delete_item(item_id):
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
    try:
        item = Item.query.get(item_id)
        if not item:
            return jsonify({"message": "Item not found"}), 404

        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item deleted successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

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
    
    # Validate input
    if not data or 'item_id' not in data or 'user_email' not in data:
        return jsonify({'message': 'Missing item_id or user_email'}), 400
    
    try:
        item_id = int(data['item_id'])  # Ensure item_id is an integer
    except ValueError:
        return jsonify({'message': 'Invalid item_id format'}), 400
    
    user_email = data['user_email'].strip()  # Clean whitespace
    
    # Find active transaction
    transaction = db.session.query(BorrowTransaction).\
        filter(
            BorrowTransaction.item_id == item_id,
            BorrowTransaction.user_email == user_email,
            BorrowTransaction.return_date.is_(None)
        ).first()
    
    if not transaction:
        return jsonify({'message': 'No active borrowing record found'}), 404
    
    try:
        # Update transaction and item
        transaction.return_date = datetime.utcnow()
        transaction.item.status = 'available'
        db.session.commit()
        
        # Refresh objects to get updated data
        db.session.refresh(transaction)
        db.session.refresh(transaction.item)
        
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
        print(f"Error returning item: {e}")  # Log the error
        return jsonify({'message': 'Failed to process return'}), 500

# Populate books
@items_bp.route('/populate', methods=['POST'])
def populate_books():
    try:
        # Hardcoded book data
        books = [
            {"title": "1984", "author": "George Orwell", "pub_year": 1949, "status": "available", "type": "book"},
            {"title": "To Kill a Mockingbird", "author": "Harper Lee", "pub_year": 1960, "status": "available", "type": "book"},
            {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "pub_year": 1925, "status": "available", "type": "book"},
            {"title": "Pride and Prejudice", "author": "Jane Austen", "pub_year": 1813, "status": "available", "type": "book"}
        ]

        # Insert books into the database
        for book in books:
            new_item = Item(
                title=book["title"],
                author=book["author"],
                pub_year=book["pub_year"],
                status=book["status"],
                type=book["type"]
            )
            db.session.add(new_item)
        db.session.commit()

        return jsonify({"message": f"{len(books)} books populated successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500
