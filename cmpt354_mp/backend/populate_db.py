# from models import db, User, Book, Events, Staff, Volunteer

# with app.app_context():
#     db.drop_all()
#     db.create_all()

#     # Sample users
#     u1 = User(name='Alice', email='alice@example.com', password='123', role='user')
#     u2 = User(name='Bob', email='bob@example.com', password='123', role='staff')

#     db.session.add_all([u1, u2])
#     db.session.commit()

#     # # Sample books
#     # books_data = [
#     #     {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year_published": 1925, "borrowed": True},
#     #     {"title": "1984", "author": "George Orwell", "year_published": 1949, "borrowed": False},
#     #     # Add more books as needed
#     # ]

#     # for book_data in books_data:
#     #     book = Book(
#     #         title=book_data['title'],
#     #         author=book_data['author'],
#     #         year_published=book_data['year_published'],
#     #         borrowed=book_data['borrowed']
#     #     )
#     #     db.session.add(book)

#     db.session.commit()
#     print("Database populated successfully!")
