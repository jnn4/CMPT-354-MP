from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To disable unnecessary warnings

# Initialize the database object
db = SQLAlchemy(app)

# Define the User model based on your SQL table schema
class User(db.Model):
    __tablename__ = 'Users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.name}, Email {self.email}>'

# Create all the tables based on the defined models
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
