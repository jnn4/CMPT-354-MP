from flask import Flask
from flask_cors import CORS
from extensions import db  # Import db from extensions
from models import Person, User, Staff, Volunteer, Room, Event, Audience, Item, FutureItem, BorrowTransaction, Fines, RequestHelp
from datetime import datetime, date, time
from werkzeug.security import generate_password_hash
import requests

# Initialize Flask app
app = Flask(__name__)

# Configure CORS
CORS(app, resources={
    r"/*": {
        "origins": "http://localhost:5173",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'I-LOVE-DB'

# Initialize db with app
db.init_app(app)

# Import and register Blueprints (do this *before* app setup)
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.items import items_bp
from routes.user import user_bp
from routes.staff import staff_bp
from routes.events import events_bp
from routes.rooms import rooms_bp
from routes.transactions import transactions_bp
from routes.requests_help import requests_help_bp
from routes.future_items import future_items_bp
from routes.fines import fines_bp
from routes.person import person_bp
from routes.volunteer import volunteer_bp
from routes.audience import audience_bp

# Register blueprints (/routes)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(dashboard_bp)
app.register_blueprint(items_bp, url_prefix='/items')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(staff_bp, url_prefix='/staff')
app.register_blueprint(events_bp)
app.register_blueprint(rooms_bp, url_prefix='/rooms')
app.register_blueprint(transactions_bp, url_prefix='/transactions')
app.register_blueprint(requests_help_bp, url_prefix='/requests_help')
app.register_blueprint(future_items_bp, url_prefix='/future_items')
app.register_blueprint(volunteer_bp, url_prefix='/volunteer')
app.register_blueprint(fines_bp, url_prefix='/fines')
app.register_blueprint(person_bp, url_prefix='/person')
app.register_blueprint(audience_bp, url_prefix='/audience')

def populate_database():
    """Populate all tables with sample data using existing populate endpoints"""
    print("Starting database population...")
    
    # Create a test client
    with app.test_client() as client:
        try:
            # Populate Users
            response = client.post('/auth/populate_test_user')
            if response.status_code == 200:
                print("✓ Users populated")
            else:
                print(f"✗ Failed to populate Users: {response.status_code} - {response.get_json()}")

            # Populate Items
            response = client.post('/items/populate_items')
            if response.status_code == 200:
                print("✓ Items populated")
            else:
                print(f"✗ Failed to populate Items: {response.status_code} - {response.get_json()}")

            # Populate Events
            response = client.post('/events/populate_events')
            if response.status_code == 200:
                print("✓ Events populated")
            else:
                print(f"✗ Failed to populate Events: {response.status_code} - {response.get_json()}")

            # Populate Future Items
            response = client.post('/future_items/populate')
            if response.status_code == 200:
                print("✓ Future Items populated")
            else:
                print(f"✗ Failed to populate Future Items: {response.status_code} - {response.get_json()}")

            # Populate Transactions
            response = client.post('/transactions/populate')
            if response.status_code == 200:
                print("✓ Transactions populated")
            else:
                print(f"✗ Failed to populate Transactions: {response.status_code} - {response.get_json()}")

            # Populate Fines
            response = client.post('/fines/populate')
            if response.status_code == 200:
                print("✓ Fines populated")
            else:
                print(f"✗ Failed to populate Fines: {response.status_code} - {response.get_json()}")

            # Populate Volunteers
            response = client.post('/volunteer/populate')
            if response.status_code == 200:
                print("✓ Volunteers populated")
            else:
                print(f"✗ Failed to populate Volunteers: {response.status_code} - {response.get_json()}")

            print("\nDatabase population completed!")

        except Exception as e:
            print(f"Error during database population: {str(e)}")
            import traceback
            print(traceback.format_exc())

# Create the tables in the database if they don't exist
with app.app_context():
    db.create_all()
    populate_database()

if __name__ == '__main__':
    app.run(debug=True, port=8000)
