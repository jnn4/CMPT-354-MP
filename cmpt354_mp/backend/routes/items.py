from flask import Blueprint, jsonify, request
from models import db, Item

items_bp = Blueprint('items', __name__)

# Create a new item
@items_bp.route('/', methods=['POST'])
def create_item():
    try:
        data = request.get_json()
        
        # Create new item
        new_item = Item(
            title=data['title'],
            author=data['author'],
            pub_year=data.get('pub_year'),
            status=data['status'],
            type=data['type']
        )
        
        db.session.add(new_item)
        db.session.commit()
        
        return jsonify({
            "message": "Item created successfully",
            "item_id": new_item.item_id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to create item", "error": str(e)}), 500

# Get all items
@items_bp.route('/', methods=['GET'])
def get_items():
    items = Item.query.all()
    items_data = [
        {
            "id": items.item_id,
            "title": items.title,
            "author": items.author,
            "year_published": items.pub_year,
            "borrowed": items.status,
            "type": items.type
        }
        for items in items
    ]
    return jsonify(items_data), 200

# Populate the database with a set of items
@items_bp.route('/populate_items', methods=['POST'])
def populate_items():
    try:
        items_data = [
            {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "pub_year": 1951, "status": "available", "type": "book"},
            {"title": "Abbey Road", "author": "The Beatles", "pub_year": 1969, "status": "borrowed", "type": "cd"},
            {"title": "National Geographic - Space Edition", "author": "National Geographic", "pub_year": 2023, "status": "available", "type": "magazine"},
            {"title": "To Kill a Mockingbird", "author": "Harper Lee", "pub_year": 1960, "status": "available", "type": "book"},
            {"title": "The Godfather", "author": "Mario Puzo", "pub_year": 1969, "status": "borrowed", "type": "book"},
            {"title": "Dark Side of the Moon", "author": "Pink Floyd", "pub_year": 1973, "status": "available", "type": "cd"},
            {"title": "Time Magazine - AI Issue", "author": "Time Magazine", "pub_year": 2024, "status": "available", "type": "magazine"},
            {"title": "1984", "author": "George Orwell", "pub_year": 1949, "status": "borrowed", "type": "book"},
            {"title": "The Subtle Art of Not Giving a F*ck", "author": "Mark Manson", "pub_year": 2016, "status": "available", "type": "book"},
            {"title": "The Rolling Stones - Greatest Hits", "author": "The Rolling Stones", "pub_year": 2002, "status": "borrowed", "type": "cd"}
        ]


        for items_data in items_data:
            item = Item(**items_data)
            db.session.add(item)
        
        db.session.commit()
        return jsonify({"message": "Items populated successfully"}), 200
    
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")  # Logs the error in your terminal
        return jsonify({"message": "Failed to populate Items", "error": str(e)}), 500

# Borrow a Item by its ID
@items_bp.route('/items/borrow/<int:id>', methods=['PATCH'])
def borrow_item(id):
    item = Item.query.get(id)
    if not item:
        return jsonify({"message": "Item not found"}), 404

    if item.borrowed:
        return jsonify({"message": "This item is already borrowed"}), 400

    item.borrowed = True
    db.session.commit()

    return jsonify({
        "message": "Item borrowed successfully",
        "item": {"id": item.id, "title": item.title}
    }), 200

# Return a borrowed Item by its ID
@items_bp.route('/item/return/<int:id>', methods=['PATCH'])
def return_item(id):
    item = Item.query.get(id)
    if not item:
        return jsonify({"message": "Item not found"}), 404

    if not item.borrowed:
        return jsonify({"message": "This item was not borrowed"}), 400

    item.borrowed = False
    db.session.commit()

    return jsonify({
        "message": "Item returned successfully",
        "Item": {"id": item.id, "title": item.title}
    }), 200
