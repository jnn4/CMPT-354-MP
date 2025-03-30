from flask import Flask
from flask_cors import CORS
from extensions import db  # Import db from extensions
from models import User  # Import the User model
from models import Book  # Import the Book model


# Initialize Flask app
app = Flask(__name__)

CORS(app, resources={r"/*": {
    "origins": "http://localhost:5173",
    "methods": ["GET", "POST", "OPTIONS", "PATCH"],  # fixes the CORs requests magically!
    "allow_headers": ["Content-Type", "Authorization"]
}})

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///librarytest.db'
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

# Register blueprints (/routes)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(dashboard_bp)
app.register_blueprint(items_bp, url_prefix='/items')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
