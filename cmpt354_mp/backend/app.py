from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy 
from flask_cors import CORS  # Import CORS

app = Flask(__name__)

# Enable CORS for the entire app
CORS(app)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///librarytest.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# DEFINING DATABASE MODELS
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

class Volunteer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String(100), nullable=False)

# Create the database and tables
with app.app_context():
    db.create_all()

# Home route
@app.route('/')
def index():
    return "Welcome to the Library API!"

# GETTING DATA FROM DATABASE
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

# Route to get all events
@app.route('/api/events', methods=['GET'])
def get_events():
    events = Events.query.all()
    events_list = [{"id": event.id, 
                   "title": event.title, 
                   "description": event.description, 
                   "date": event.date,
                   "rsvp": event.rsvp} for event in events]
    return jsonify(events_list)

# Route to get all staff members
@app.route('/api/staff', methods=['GET'])
def get_staff():
    staff = Staff.query.all()
    staff_list = [{"id": staff_member.id, 
                   "name": staff_member.name, 
                   "position": staff_member.position} for staff_member in staff]
    return jsonify(staff_list)

# Route to get all Volunteer positions
@app.route('/api/volunteer', methods=['GET'])
def get_volunteer():
    volunteer_positions = Volunteer.query.all()
    volunteer_positions = [{"id": volunteer.id,
                            "position": volunteer.position} for volunteer in volunteer_positions]
    return jsonify(volunteer_positions)

# POPULATING DATABASE
@app.route('/api/books/populate_books', methods=['POST'])
def populate_books():
    # Check if the database already has staff members
    existing_books = Book.query.first()  # If any staff member exists, skip population
    if existing_books:
        return jsonify({"message": "Staff members already exist!"}), 200

    # Example books data (10 books)
    books_data = [
        {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year_published": 1925, "borrowed": True},
        {"title": "1984", "author": "George Orwell", "year_published": 1949, "borrowed": False},
        {"title": "To Kill a Mockingbird", "author": "Harper Lee", "year_published": 1960, "borrowed": True},
        {"title": "Pride and Prejudice", "author": "Jane Austen", "year_published": 1813, "borrowed": False},
        {"title": "Moby-Dick", "author": "Herman Melville", "year_published": 1851, "borrowed": False},
        {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "year_published": 1951, "borrowed": True},
        {"title": "The Hobbit", "author": "J.R.R. Tolkien", "year_published": 1937, "borrowed": False},
        {"title": "War and Peace", "author": "Leo Tolstoy", "year_published": 1869, "borrowed": True},
        {"title": "The Odyssey", "author": "Homer", "year_published": -800, "borrowed": False},
        {"title": "Crime and Punishment", "author": "Fyodor Dostoevsky", "year_published": 1866, "borrowed": True}
    ]

    # Add books to the database
    for book_data in books_data:
        book = Book(
            title=book_data['title'],
            author=book_data['author'],
            year_published=book_data['year_published'],
            borrowed=book_data['borrowed']
        )
        db.session.add(book)
    
    db.session.commit()
    return jsonify({"message": "Database populated with 10 books!"}), 200


@app.route('/api/events/populate_events', methods=['POST'])
def populate_events():
    # Check if the database already has staff members
    existing_events = Events.query.first()  # If any staff member exists, skip population
    if existing_events:
        return jsonify({"message": "events members already exist!"}), 200

    # Example events data (10 events)
    events_data = [
        {"title": "Book Club", "description": "Monthly book discussion", "date": "2023-10-01", "rsvp": True},
        {"title": "Author Meet and Greet", "description": "Meet your favorite authors", "date": "2023-11-01", "rsvp": False},
        {"title": "Library Tour", "description": "Guided tour of the library", "date": "2023-09-15", "rsvp": True},
        {"title": "Children's Story Time", "description": "Reading for young children", "date": "2023-10-10", "rsvp": False},
        {"title": "Reading Challenge", "description": "Annual reading competition", "date": "2023-12-01", "rsvp": True},
        {"title": "Poetry Slam", "description": "Performance poetry event", "date": "2023-11-20", "rsvp": False},
        {"title": "Book Signing", "description": "Meet the author of your favorite book", "date": "2023-10-25", "rsvp": True},
        {"title": "Library Volunteer Day", "description": "Help organize the library", "date": "2023-11-15", "rsvp": False},
        {"title": "Book Sale", "description": "Annual book sale event", "date": "2023-12-05", "rsvp": True},
        {"title": "Digital Literacy Workshop", "description": "Learn how to use online resources", "date": "2023-09-30", "rsvp": False}
    ]

    # Add events to the database
    for event_data in events_data:
        event = Events(
            title=event_data['title'],
            description=event_data['description'],
            date=event_data['date'],
            rsvp=event_data['rsvp']
        )
        db.session.add(event)
    
    db.session.commit()
    return jsonify({"message": "Database populated with 10 events!"}), 200


@app.route('/api/staff/populate_staff', methods=['POST'])
def populate_staff():
    # Check if the database already has staff members
    existing_staff = Staff.query.first()  # If any staff member exists, skip population
    if existing_staff:
        return jsonify({"message": "Staff members already exist!"}), 200
    
    # Example staff data (2 staff members)
    staff_data = [
        {"name": "John Doe", "position": "Librarian"},
        {"name": "Jane Smith", "position": "Assistant Librarian"},
        {"name": "Robert Brown", "position": "Library Assistant"},
        {"name": "Emily White", "position": "Library Technician"},
        {"name": "Michael Green", "position": "Head of Circulation"},
        {"name": "Sara Blue", "position": "Events Coordinator"},
        {"name": "David Black", "position": "Security Guard"},
        {"name": "Laura Gray", "position": "Volunteer Coordinator"},
        {"name": "James Red", "position": "Cataloging Specialist"},
        {"name": "Olivia Yellow", "position": "Library Outreach Manager"}
    ]

    # Add staff members to the database
    for staff_member_data in staff_data:
        staff_member = Staff(
            name=staff_member_data['name'],
            position=staff_member_data['position']
        )
        db.session.add(staff_member)
    
    db.session.commit()
    return jsonify({"message": "Database populated with staff!"}), 200


@app.route('/api/volunteer/populate_volunteer', methods=['POST'])
def populate_volunteers():
    # Check if the database already has volunteer positions
    existing_volunteer = Volunteer.query.first()  # If any volunteer position exists, skip population
    if existing_volunteer:
        return jsonify({"message": "Volunteer positions already exist!"}), 200
    
    # Example volunteer positions data (2 volunteers)
    volunteer_data = [
        {"position": "Book Organizer"},
        {"position": "Event Coordinator"}
    ]

    # Add volunteer positions to the database
    for volunteer_position_data in volunteer_data:
        volunteer_position = Volunteer(
            position=volunteer_position_data['position']
        )
        db.session.add(volunteer_position)
    
    db.session.commit()
    return jsonify({"message": "Database populated with volunteer positions!"}), 200


# Route to add a new book
@app.route('/api/books/add', methods=['POST'])
def add_book():
    # Get data from the request body (expected to be in JSON format)
    data = request.get_json()

    # Extract information from the request data
    title = data.get('title')
    author = data.get('author')
    year_published = data.get('year_published')
    borrowed = data.get('borrowed')

    # Check if all necessary fields are provided
    if not title or not author or not year_published or borrowed is None:
        return jsonify({"message": "Missing required fields"}), 400  # Return error if fields are missing

    try:
        # Create a new book entry in the database (adjust the model as needed)
        new_book = Book(title=title, author=author, year_published=year_published, borrowed=borrowed)

        # Add the new book to the database
        db.session.add(new_book)
        db.session.commit()  # Commit the transaction

        # Return a success message
        return jsonify({"message": "Book added successfully!"}), 201  # 201 indicates successful creation
    except Exception as e:
        # Handle any errors (e.g., database issues)
        print(f"Error: {e}")
        return jsonify({"message": "Error adding book"}), 500  # Return a 500 error if something goes wrong


@app.route('/api/events/add', methods=['POST'])
def add_event():
    # Check if any event already exists
    existing_events = Events.query.first()  # Check if any event exists
    if existing_events:  
        return jsonify({"message": "Events already exist!"}), 200
    
    # Create a new event
    event = Events(title="Book Club", description="Monthly book discussion", date="2023-10-01", rsvp=True)
    db.session.add(event)
    db.session.commit()
    return jsonify({"message": "Event added successfully!"}), 201

@app.route('/api/staff/add', methods=['POST'])
def add_staff():
    # Check if any staff member already exists
    existing_staff = Staff.query.first()  # Check if any staff member exists
    if existing_staff:  
        return jsonify({"message": "Staff members already exist!"}), 200
    
    # Create a new staff member
    staff_member = Staff(name="John Doe", position="Librarian")
    db.session.add(staff_member)
    db.session.commit()
    return jsonify({"message": "Staff member added successfully!"}), 201

@app.route('/api/volunteer/add', methods=['POST'])
def add_volunteer():
    # Check if any volunteer position already exists
    existing_volunteer = Volunteer.query.first()  # Check if any volunteer position exists
    if existing_volunteer:  
        return jsonify({"message": "Volunteer positions already exist!"}), 200
    
    # Create a new volunteer position
    volunteer_position = Volunteer(position="Book Organizer")
    db.session.add(volunteer_position)
    db.session.commit()
    return jsonify({"message": "Volunteer position added successfully!"}), 201

if __name__ == '__main__':
    app.run(debug=True, port = 8000)
