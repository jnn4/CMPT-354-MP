from flask import Flask
from flask_cors import CORS
from extensions import db  # Import db from extensions
from models import Person, User, Staff, Volunteer, Item, BorrowTransaction, Fine, Room, Event, RequestHelp, FutureItem

# Initialize Flask app
app = Flask(__name__)

CORS(
    app,
    resources={r"/*": {
        "origins": "http://localhost:5173",  # Your frontend URL
        "methods": ["GET", "POST", "OPTIONS", "PATCH"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True  # For cookies/session
    }}
)


# Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'I-LOVE-DB'

# Initialize db with app
db.init_app(app)

# Create the tables in the database if they don't exist
with app.app_context():
    db.create_all()

# Import and register Blueprints (do this *after* app and db setup)
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.items import items_bp
from routes.events import events_bp
from routes.requests_help import requests_help_bp
from routes.volunteer import volunteer_bp
from routes.donate import donate_bp

# Register blueprints (/routes)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(dashboard_bp)

app.register_blueprint(items_bp, url_prefix='/items')
app.register_blueprint(events_bp, url_prefix='/events')
app.register_blueprint(requests_help_bp, url_prefix='/requests_help')
app.register_blueprint(volunteer_bp, url_prefix='/volunteer')
app.register_blueprint(donate_bp, url_prefix='/donate')

@app.cli.command("insert-test-data")
def insert_test_data_command():
    """Insert test data into the database"""
    from insert_test_data import insert_test_data
    insert_test_data()
    print("Test data inserted!")

if __name__ == '__main__':
    app.run(debug=True, port=8000)
