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
    books_list = [{"id": book.id, "title": book.title, "author": book.author, "year_published": book.year_published} for book in books]
    return jsonify(books_list)

# Route to add a new book
@app.route('/api/books/add', methods=['POST'])
def add_book():
    book = Book(title="The Great Gatsby", author="F. Scott Fitzgerald", year_published=1925)
    db.session.add(book)
    db.session.commit()
    return jsonify({"message": "Book added successfully!"}), 201

if __name__ == '__main__':
    app.run(debug=True)
