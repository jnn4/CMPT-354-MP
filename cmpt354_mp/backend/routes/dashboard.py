from flask import Blueprint

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def home():
    return 'Welcome to the dashboard!'

@dashboard_bp.route('/login', methods=['OPTIONS'])
def handle_options():
    return '', 200
    
# from flask import jsonify
# from app import app
# from models import Book, Events, Staff, Volunteer

# Route to get all books
# @app.route('/api/books', methods=['GET'])
# def get_books():
#     books = Book.query.all()
#     books_list = [{"id": book.id, 
#                    "title": book.title, 
#                    "author": book.author, 
#                    "year_published": book.year_published,
#                    "borrowed": book.borrowed} for book in books]
#     return jsonify(books_list)

# Route to get all events
# @app.route('/api/events', methods=['GET'])
# def get_events():
#     events = Events.query.all()
#     events_list = [{"id": event.id, 
#                     "title": event.title, 
#                     "description": event.description, 
#                     "date": event.date,
#                     "rsvp": event.rsvp} for event in events]
#     return jsonify(events_list)

# # Route to get all staff members
# @app.route('/api/staff', methods=['GET'])
# def get_staff():
#     staff = Staff.query.all()
#     staff_list = [{"id": staff_member.id, 
#                    "name": staff_member.name, 
#                    "position": staff_member.position} for staff_member in staff]
#     return jsonify(staff_list)

# # Route to get all volunteer positions
# @app.route('/api/volunteer', methods=['GET'])
# def get_volunteer():
#     volunteer_positions = Volunteer.query.all()
#     volunteer_positions = [{"id": volunteer.id,
#                             "position": volunteer.position} for volunteer in volunteer_positions]
#     return jsonify(volunteer_positions)
