# storing here temporarily

# from models import db, User, Book

# # Create sample users
# u1 = User(name="John Doe", email="johndoe@example.com", password_hash="hashedpassword1", role="user")
# u2 = User(name="Jane Smith", email="janesmith@example.com", password_hash="hashedpassword2", role="user")

# # Sample books data
# books_data = [
#     {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year_published": 1925, "borrowed": True},
#     {"title": "1984", "author": "George Orwell", "year_published": 1949, "borrowed": False},
#     {"title": "Moby Dick", "author": "Herman Melville", "year_published": 1851, "borrowed": False},
#     {"title": "To Kill a Mockingbird", "author": "Harper Lee", "year_published": 1960, "borrowed": True}
# ]

# with app.app_context():
#     # db.drop_all()  # Drops all tables (be careful with this)
#     # db.create_all()  # Creates the tables

#     # Add sample users to the database
#     db.session.add_all([u1, u2])
#     db.session.commit()  # Commit the users to save in the database

#     # Create and add books, associate them with users
#     for book_data in books_data:
#         book = Book(
#             title=book_data['title'],
#             author=book_data['author'],
#             year_published=book_data['year_published'],
#             borrowed=book_data['borrowed'],
#             user_id=u1.user_id if book_data['borrowed'] else u2.user_id  # Assign the book to the first user if borrowed
#         )
#         db.session.add(book)

#     db.session.commit()  # Commit the books to save in the database
#     print("Database populated successfully!")

# @api_bp.route('/books', methods=['GET'])
# def get_books():
#     books = Book.query.all()
#     books_list = [{"id": book.id, 
#                    "title": book.title, 
#                    "author": book.author, 
#                    "year_published": book.year_published,
#                    "borrowed": book.borrowed} for book in books]
#     return jsonify(books_list)

# @api_bp.route('/events', methods=['GET'])
# def get_events():
#     events = Events.query.all()
#     events_list = [{"id": event.id, 
#                     "title": event.title, 
#                     "description": event.description, 
#                     "date": event.date,
#                     "rsvp": event.rsvp} for event in events]
#     return jsonify(events_list)

# @api_bp.route('/staff', methods=['GET'])
# def get_staff():
#     staff = Staff.query.all()
#     staff_list = [{"id": staff_member.id, 
#                    "name": staff_member.name, 
#                    "position": staff_member.position} for staff_member in staff]
#     return jsonify(staff_list)

# @api_bp.route('/volunteer', methods=['GET'])
# def get_volunteer():
#     volunteer_positions = Volunteer.query.all()
#     volunteer_positions_list = [{"id": volunteer.id,
#                                  "position": volunteer.position} for volunteer in volunteer_positions]
#     return jsonify(volunteer_positions_list)
