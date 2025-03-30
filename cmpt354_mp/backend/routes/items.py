from flask import Flask, Blueprint, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import Book
from app import db  # Import db from app.py

items_bp = Blueprint('items', __name__)

@items_bp.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    books_data = [{"id": book.id, "title": book.title, "author": book.author,
                   "year_published": book.year_published, "borrowed": book.borrowed}
                  for book in books]
    return jsonify(books_data)

@items_bp.route('/books/populate_books', methods=['POST'])
def populate_books():
    try:
        books_data = [
            {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year_published": 1925, "borrowed": False},
            {"title": "1984", "author": "George Orwell", "year_published": 1949, "borrowed": False},
            {"title": "Moby Dick", "author": "Herman Melville", "year_published": 1851, "borrowed": False},
            {"title": "To Kill a Mockingbird", "author": "Harper Lee", "year_published": 1960, "borrowed": False},
        ]

        for book_data in books_data:
            book = Book(**book_data)
            db.session.add(book)
        
        db.session.commit()
        return jsonify({"message": "Books populated successfully"}), 200
    
    except Exception as e:
        print(f"Error: {e}")  # Logs the error in your terminal
        return jsonify({"message": "Failed to populate books", "error": str(e)}), 500

@items_bp.route('/books/borrow/<int:id>', methods=['PATCH'])
def borrow_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"message": "Book not found"}), 404

    if book.borrowed:
        return jsonify({"message": "This book is already borrowed"}), 400

    book.borrowed = True
    db.session.commit()

    return jsonify({"message": "Book borrowed successfully", "book": {"id": book.id, "title": book.title}}), 200
