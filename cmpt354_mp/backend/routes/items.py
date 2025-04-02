from flask import Blueprint, jsonify, request
from models import db, Item  # Import Item model instead of Book model

items_bp = Blueprint('items', __name__)

# Get all items
@items_bp.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    items_data = [
        {
            "id": item.item_id,
            "title": item.title,
            "author": item.author,
            "pub_year": item.pub_year,
            "status": item.status,
            "type": item.type
        }
        for item in items
    ]
    return jsonify(items_data)

# Populate the database with a set of items
@items_bp.route('/items/populate_items', methods=['POST'])
def populate_items():
    try:
        items_data = [
            {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "pub_year": 1925, "status": "available", "type": "book"},
            {"title": "1984", "author": "George Orwell", "pub_year": 1949, "status": "available", "type": "book"},
            {"title": "Moby Dick", "author": "Herman Melville", "pub_year": 1851, "status": "available", "type": "book"},
            {"title": "To Kill a Mockingbird", "author": "Harper Lee", "pub_year": 1960, "status": "available", "type": "book"},
        ]


        for item_data in items_data:
            item = Item(**item_data)
            db.session.add(item)
        
        db.session.commit()
        return jsonify({"message": "Items populated successfully"}), 200
    
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")  # Logs the error in your terminal
        return jsonify({"message": "Failed to populate items", "error": str(e)}), 500

# Borrow an item by its ID
@items_bp.route('/items/borrow/<int:id>', methods=['PATCH'])
def borrow_item(id):
    item = Item.query.get(id)
    if not item:
        return jsonify({"message": "Item not found"}), 404

    if item.status == "borrowed":
        return jsonify({"message": "This item is already borrowed"}), 400

    item.status = "borrowed"
    db.session.commit()

    return jsonify({
        "message": "Item borrowed successfully",
        "item": {"id": item.item_id, "title": item.title}
    }), 200

# Return a borrowed item by its ID
@items_bp.route('/items/return/<int:id>', methods=['PATCH'])
def return_item(id):
    item = Item.query.get(id)
    if not item:
        return jsonify({"message": "Item not found"}), 404

    if item.status != "borrowed":
        return jsonify({"message": "This item was not borrowed"}), 400

    item.status = "available"
    db.session.commit()

    return jsonify({
        "message": "Item returned successfully",
        "item": {"id": item.item_id, "title": item.title}
    }), 200
