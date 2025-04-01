from flask import Flask
from flask_cors import CORS
from extensions import db  # Import db from extensions
from models import Person, User, Staff, Volunteer, Room, Event, Audience, Item, FutureItem, BorrowTransaction, Fines, RequestHelp


# Initialize Flask app
app = Flask(__name__)

CORS(app, resources={r"/*": {
    "origins": "http://localhost:5173",
    "methods": ["GET", "POST", "OPTIONS", "PATCH"],  # fixes the CORs requests magically!
    "allow_headers": ["Content-Type", "Authorization"]
}})

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
app.register_blueprint(events_bp, url_prefix='/events')
app.register_blueprint(rooms_bp, url_prefix='/rooms')
app.register_blueprint(transactions_bp, url_prefix='/transactions')
app.register_blueprint(requests_help_bp, url_prefix='/requests_help')
app.register_blueprint(future_items_bp, url_prefix='/future_items')
app.register_blueprint(volunteer_bp, url_prefix='/volunteer')
app.register_blueprint(fines_bp, url_prefix='/fines')
app.register_blueprint(person_bp, url_prefix='/person')
app.register_blueprint(audience_bp, url_prefix='/audience')



if __name__ == '__main__':
    app.run(debug=True, port=8000)
