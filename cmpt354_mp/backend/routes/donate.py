from flask import Blueprint, request, jsonify
from extensions import db
from flask_cors import CORS  # Ensure CORS is imported
from models import Person, User, Staff, Item, FutureItem, donates
from datetime import datetime

# Create Blueprint for authentication routes
donate_bp = Blueprint('donates', __name__)

# Enable CORS for all routes in the Blueprint
CORS(donate_bp, resources={
    r"/*": {
        "origins": "http://localhost:5173",
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Donate items
@donate_bp.route('', methods=['POST'], strict_slashes=False)
def donate_item():
    data = request.json
    user_email = data.get('user_email')
    
    try:
        # Create new item
        new_item = Item(
            title=data['title'],
            author=data['author'],
            pub_year=data.get('pub_year'),
            type=data['type'],
            status='pending'
        )
        
        db.session.add(new_item)
        db.session.flush()  # Get the generated item_id
        
        # Create future item entry
        new_future = FutureItem(
            arrival_date=datetime.strptime(data['arrival_date'], '%Y-%m-%d').date(),
            item_id=new_item.item_id
        )
        db.session.add(new_future)
        
        # Record donation
        db.session.execute(donates.insert().values(
            user_email=user_email,
            item_id=new_item.item_id,
            donation_status='pending',
            donation_date=datetime.utcnow().date()
        ))
        
        db.session.commit()
        return jsonify({
            'message': 'Donation recorded successfully',
            'item_id': new_item.item_id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

