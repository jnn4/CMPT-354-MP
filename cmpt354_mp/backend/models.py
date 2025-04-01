from extensions import db
from datetime import datetime

# Person Table
class Person(db.Model):
    __tablename__ = 'person'
    
    email = db.Column(db.String(100), primary_key=True)  # Unique identifier
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone_num = db.Column(db.String(20), nullable=True)
    age = db.Column(db.Integer, nullable=True)

    user = db.relationship('User', backref=db.backref('person', uselist=False))
    staff = db.relationship('Staff',backref=db.backref('person', uselist=False))



# User model
class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), db.ForeignKey('person.email'), unique=True, nullable=False)  # FK to Person
    password = db.Column(db.String(255), nullable=False)  # Hashed password
    
    # Relationship with Borrow Transactions
    # BorrowTransaction = db.relationship('BorrowTransaction', backref=db.backref('person', uselist=False))

    borrow_transactions = db.relationship(
        "BorrowTransaction",
        back_populates="person"
    )

    def __init__(self, email, password, role='user'):
        self.email = email
        self.password = password  # Store hashed password
        self.role = role

# Staff Table
class Staff(db.Model):
    __tablename__ = 'staff'
    
    staff_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), db.ForeignKey('person.email'), nullable=False, unique=True)
    position = db.Column(db.String(100), nullable=False)
    wage = db.Column(db.Float, nullable=True)
    password = db.Column(db.String(255), nullable=False)  # Hashed password

# Volunteer Table
class Volunteer(db.Model):
    __tablename__ = 'volunteer'
    
    volunteer_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'), primary_key=True)
    role = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)

# Room Table
class Room(db.Model):
    __tablename__ = 'room'
    
    room_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    capacity = db.Column(db.Integer, nullable=False)

# Event Table
class Event(db.Model):
    __tablename__ = 'event'
    
    event_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    event_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.room_id'), nullable=True)

    room = db.relationship('Room', backref=db.backref('events', uselist=False))

# Audience Table
class Audience(db.Model):
    __tablename__ = 'audience'
    
    aud_id = db.Column(db.Integer, primary_key=True)
    min_age = db.Column(db.Integer, nullable=False)
    max_age = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(100), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=False)

# Item Table
class Item(db.Model):
    __tablename__ = 'item'
    
    item_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    pub_year = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)

# Future Item Table
class FutureItem(db.Model):
    __tablename__ = 'future_item'
    
    future_item_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'), nullable=False, unique=True)
    arrival_date = db.Column(db.Date, nullable=False)
    
# Borrow Transaction Table
class BorrowTransaction(db.Model):
    __tablename__ = 'borrow_transactions'

    trans_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))  # Reference to 'user' table
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'))  # Reference to 'item' table
    borrowed_at = db.Column(db.DateTime, default=datetime)

    #user = db.relationship('User', backref=db.backref('borrow_transactions', uselist=False))
    person = db.relationship(
            "User",
            back_populates="borrow_transactions"
        )

    book = db.relationship('Item', backref=db.backref('borrow_transactions', uselist=False))


# Fine Table
class Fines(db.Model):
    __tablename__ = 'fines'
    
    fine_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    paid = db.Column(db.Boolean, default=False)
    trans_id = db.Column(db.Integer, db.ForeignKey('borrow_transactions.trans_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

# Requests Help Table
class RequestHelp(db.Model):
    __tablename__ = 'request_help'
    
    request_help_id = db.Column(db.Integer, primary_key=True)
    request_text = db.Column(db.Text, nullable=False)
    response_text = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'), nullable=False)

# User attends Event (with attendance status and registration date)
attends = db.Table('attends',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('event.event_id'), primary_key=True),
    db.Column('attendance_status', db.String(50), nullable=False),
    db.Column('registration_date', db.Date, nullable=False)
)

# Event recommended to Audience
recommended = db.Table('recommended',
    db.Column('aud_id', db.Integer, db.ForeignKey('audience.aud_id'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('event.event_id'), primary_key=True)
)

# Event held in Room
held_in = db.Table('held_in',
    db.Column('room_id', db.Integer, db.ForeignKey('room.room_id'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('event.event_id'), primary_key=True)
)

# Event managed by Staff
manages = db.Table('manages',
    db.Column('staff_id', db.Integer, db.ForeignKey('staff.staff_id'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('event.event_id'), primary_key=True)
)

# Volunteer assists Staff
assists = db.Table('assists',
    db.Column('staff_id', db.Integer, db.ForeignKey('staff.staff_id'), primary_key=True),
    db.Column('volunteer_id', db.Integer, db.ForeignKey('volunteer.volunteer_id'), primary_key=True)
)

# User requests help from Staff
requests = db.Table('requests',
    db.Column('staff_id', db.Integer, db.ForeignKey('staff.staff_id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
)

# User donates Item
donates = db.Table('donates',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True),
    db.Column('item_id', db.Integer, db.ForeignKey('item.item_id'), primary_key=True),
    db.Column('donation_status', db.String(50), nullable=False),
    db.Column('donation_date', db.Date, nullable=False)
)

# User creates Borrow Transaction
creates = db.Table('creates',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True),
    db.Column('trans_id', db.Integer, db.ForeignKey('borrow_transactions.trans_id'), primary_key=True)
)

# Borrow Transaction borrows Item
borrows = db.Table('borrows',
    db.Column('item_id', db.Integer, db.ForeignKey('item.item_id'), primary_key=True),
    db.Column('trans_id', db.Integer, db.ForeignKey('borrow_transactions.trans_id'), primary_key=True)
)

# Borrow Transaction has Fine when past due
is_due = db.Table('is_due',
    db.Column('trans_id', db.Integer, db.ForeignKey('borrow_transactions.trans_id'), primary_key=True),
    db.Column('fine_id', db.Integer, db.ForeignKey('fines.fine_id'), primary_key=True)
)

# # Book model
# class Book(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     author = db.Column(db.String(100), nullable=False)
#     year_published = db.Column(db.Integer, nullable=True)
#     borrowed = db.Column(db.Boolean, default=False)

#     # Foreign key to the User model (many-to-one relationship)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    
#     # You can add a backref to access the User who borrowed the book
#     # user = db.relationship('User', backref=db.backref('borrowed_books', lazy=True))

# # Commented out for now! easier for debugging

# # # Event model
# class Event(db.Model):
#     event_id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.String(500), nullable=False)
#     date = db.Column(db.DateTime, nullable=False)

#     attendees = db.relationship('User', secondary='event_attendance', back_populates='events')

# # Many-to-Many relationship for event attendance
# event_attendance = db.Table(
#     'event_attendance',
#     db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'), primary_key=True),
#     db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
# )

# # Staff model
# class Staff(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     position = db.Column(db.String(100), nullable=False)

# # Volunteer model
# class Volunteer(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     position = db.Column(db.String(100), nullable=False)
