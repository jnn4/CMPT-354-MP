from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # Import CORS

app = Flask(__name__)

# Enable CORS for the entire app
CORS(app)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///librarytest.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year_published = db.Column(db.Integer, nullable=True)
    borrowed = db.Column(db.Boolean, default=False)

class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    rsvp = db.Column(db.Boolean, default=False)

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)


# Create the database and tables
with app.app_context():
    db.create_all()

# Home route
@app.route('/')
def index():
    return "Welcome to the Library API!"

# Route to get all books
@app.route('/api/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    books_list = [{"id": book.id, 
                   "title": book.title, 
                   "author": book.author, 
                   "year_published": book.year_published,
                   "borrowed": book.borrowed} for book in books]
    return jsonify(books_list)

@app.route('api/events', methods=['GET'])
def get_events():
    events = Events.query.all()
    events_list = [{"id": event.id, 
                   "title": event.title, 
                   "description": event.description, 
                   "date": event.date,
                   "rsvp": event.rsvp} for event in events]
    return jsonify(events_list)

@app.route('api/staff', methods=['GET'])
def get_staff():
    staff = Staff.query.all()
    staff_list = [{"id": staff_member.id, 
                   "name": staff_member.name, 
                   "position": staff_member.position} for staff_member in staff]
    return jsonify(staff_list)



# Route to add a new book
@app.route('/api/books/add', methods=['POST'])
def add_book():
    book = Book(title="The Great Gatsby", author="F. Scott Fitzgerald", year_published=1925, borrowed=True)
    db.session.add(book)
    db.session.commit()
    return jsonify({"message": "Book added successfully!"}), 201

if __name__ == '__main__':
    app.run(debug=True, port = 8000)
