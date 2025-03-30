from flask import Flask
from flask_cors import CORS
from extensions import db  # Import db from extensions
from models import User  # Import the User model

# Initialize Flask app
app = Flask(__name__)

# CORS configuration to allow all routes to accept requests from localhost:5173
CORS(app, resources={r"/*": {
    "origins": "http://localhost:5173",
    "methods": ["GET", "POST", "OPTIONS"],  # Allow OPTIONS preflight requests
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
    db.create_all()  # Creates the tables defined by models like User

# Import and register Blueprints (do this *after* app and db setup)
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(dashboard_bp)

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8000)
