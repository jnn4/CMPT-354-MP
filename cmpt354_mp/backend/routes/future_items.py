from flask import Blueprint, request, jsonify
from models import FutureItem, db
from datetime import date

future_items_bp = Blueprint('future_items', __name__, url_prefix='/future_items')

# Create a new future item (formerly donation)
@future_items_bp.route('/post', methods=['POST'])
def create_future_item():
    try:
        data = request.get_json()

        # Extract necessary data from the request
        item_id = data.get('item_id')
        arrival_date_str = data.get('arrival_date')

        # Validation
        if not item_id or not arrival_date_str:
            return jsonify({"message": "Item ID and arrival date are required!"}), 400

        # Convert string date to Python date object
        try:
            arrival_date = date.fromisoformat(arrival_date_str)
        except ValueError:
            return jsonify({"message": "Invalid date format. Please use YYYY-MM-DD format."}), 400

        # Create a new future item
        new_item = FutureItem(
            item_id=item_id,
            arrival_date=arrival_date
        )

        db.session.add(new_item)
        db.session.commit()

        return jsonify({
            "message": "Future item created successfully!",
            "future_item_id": new_item.future_item_id,
            "item_id": item_id,
            "arrival_date": arrival_date_str
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# Get all future items (formerly donations)
@future_items_bp.route('/', methods=['GET'])
def get_all_future_items():
    try:
        items = FutureItem.query.all()
        items_list = [
            {
                "future_item_id": item.future_item_id,
                "user_id": item.user_id,
                "item_name": item.item_name,
                "estimated_value": item.estimated_value,
                "status": item.status
            }
            for item in items
        ]
        return jsonify(items_list), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Get a specific future item by ID
@future_items_bp.route('/<int:future_item_id>', methods=['GET'])
def get_future_item_by_id(future_item_id):
    future_item = FutureItem.query.get(future_item_id)
    if not future_item:
        return jsonify({"message": "Item not found!"}), 404

    return jsonify({
        "future_item_id": future_item.future_item_id,
        "user_id": future_item.user_id,
        "item_name": future_item.item_name,
        "estimated_value": future_item.estimated_value,
        "status": future_item.status
    }), 200

# Update a future item (e.g., status or estimated value)
@future_items_bp.route('/<int:future_item_id>', methods=['PUT'])
def update_future_item(future_item_id):
    try:
        data = request.get_json()
        future_item = FutureItem.query.get(future_item_id)

        if not future_item:
            return jsonify({"message": "Item not found!"}), 404

        # Update the future item fields
        future_item.status = data.get('status', future_item.status)
        future_item.estimated_value = data.get('estimated_value', future_item.estimated_value)

        db.session.commit()

        return jsonify({
            "message": "Future item updated successfully!",
            "future_item_id": future_item.future_item_id,
            "status": future_item.status,
            "estimated_value": future_item.estimated_value
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# Delete a future item by ID
@future_items_bp.route('/<int:future_item_id>', methods=['DELETE'])
def delete_future_item(future_item_id):
    try:
        future_item = FutureItem.query.get(future_item_id)

        if not future_item:
            return jsonify({"message": "Item not found!"}), 404

        db.session.delete(future_item)
        db.session.commit()

        return jsonify({"message": "Future item deleted successfully!"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500
    
# Populate the Future Items table
@future_items_bp.route('/populate', methods=['POST'])
def populate_future_items():
    try:
        future_items_data = [
            {"future_item_id": 1, "item_id": 101, "arrival_date": date(2025, 2, 1)},
            {"future_item_id": 2, "item_id": 102, "arrival_date": date(2025, 3, 10)},
            {"future_item_id": 3, "item_id": 103, "arrival_date": date(2025, 4, 15)},
            {"future_item_id": 4, "item_id": 104, "arrival_date": date(2025, 5, 20)},
            {"future_item_id": 5, "item_id": 105, "arrival_date": date(2025, 6, 25)},
            {"future_item_id": 6, "item_id": 106, "arrival_date": date(2025, 7, 30)},
            {"future_item_id": 7, "item_id": 107, "arrival_date": date(2025, 8, 5)},
            {"future_item_id": 8, "item_id": 108, "arrival_date": date(2025, 9, 10)},
            {"future_item_id": 9, "item_id": 109, "arrival_date": date(2025, 10, 15)},
            {"future_item_id": 10, "item_id": 110, "arrival_date": date(2025, 11, 1)}
        ]

        for future_items_data in future_items_data:
            future_item = FutureItem(**future_items_data)
            db.session.add(future_item)

        db.session.commit()
        return jsonify({"message": "FutureItem populated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to populate FutureItems", "error": str(e)}), 500