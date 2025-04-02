from extensions import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

# ----- Base Entities -----
class Person(db.Model):
    __tablename__ = 'person'
    email = db.Column(db.String(100), primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone_num = db.Column(db.String(20))
    age = db.Column(db.Integer)

# ----- Person Subtypes -----
class User(db.Model):
    __tablename__ = 'user'
    email = db.Column(db.String(100), db.ForeignKey('person.email'), primary_key=True)
    password_hash = db.Column(db.String(128), nullable=False)  # Securely store hashed passwords

    # Relationship to Person
    person = db.relationship('Person', backref=db.backref('user', uselist=False))

    # Password hashing logic
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha256")  # Use pbkdf2:sha256

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Staff(db.Model):
    __tablename__ = 'staff'
    email = db.Column(db.String(100), db.ForeignKey('person.email'), primary_key=True)
    wage = db.Column(db.Float)
    
    # Relationships
    person = db.relationship('Person', backref=db.backref('staff', uselist=False))
    managed_events = db.relationship('Event', secondary='manages', backref='managers')

class Volunteer(db.Model):
    __tablename__ = 'volunteer'
    email = db.Column(db.String(100), db.ForeignKey('person.email'), primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    
    # Relationships
    person = db.relationship('Person', backref=db.backref('volunteer', uselist=False))
    assisted_staff = db.relationship('Staff', secondary='assists', backref='assistants')

# ----- Library Entities -----
class Item(db.Model):
    __tablename__ = 'item'
    item_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    pub_year = db.Column(db.Integer)
    status = db.Column(db.String(50), nullable=False, default='available')
    type = db.Column(db.String(50), nullable=False)
    
    # Relationships
    borrows = db.relationship('BorrowTransaction', backref='item')

class BorrowTransaction(db.Model):
    __tablename__ = 'borrow_transaction'
    trans_id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(100), db.ForeignKey('user.email'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'), nullable=False)
    borrow_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(days=14))
    return_date = db.Column(db.DateTime)
    
    # Relationships
    fines = db.relationship('Fine', backref='transaction')

class Fine(db.Model):
    __tablename__ = 'fine'
    fine_id = db.Column(db.Integer, primary_key=True)
    trans_id = db.Column(db.Integer, db.ForeignKey('borrow_transaction.trans_id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    paid = db.Column(db.Boolean, default=False)

# ----- Event System -----
class Room(db.Model):
    __tablename__ = 'room'
    room_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

class Event(db.Model):
    __tablename__ = 'event'
    event_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.room_id'), nullable=True)
    min_age = db.Column(db.Integer, nullable=False)
    max_age = db.Column(db.Integer, nullable=False)
    audience_type = db.Column(db.String(100), nullable=False)
    
    # Relationships
    room = db.relationship('Room', backref='events')

# ----- Association Tables -----
attends = db.Table('attends',
    db.Column('user_email', db.String(100), db.ForeignKey('user.email'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('event.event_id'), primary_key=True),
    db.Column('attendance_status', db.String(50), nullable=False, default='registered'),
    db.Column('registration_date', db.Date, default=datetime.utcnow)
)

donates = db.Table('donates',
    db.Column('user_email', db.String(100), db.ForeignKey('user.email'), primary_key=True),
    db.Column('item_id', db.Integer, db.ForeignKey('item.item_id'), primary_key=True),
    db.Column('donation_status', db.String(50), nullable=False),
    db.Column('donation_date', db.Date, default=datetime.utcnow)
)

manages = db.Table('manages',
    db.Column('staff_email', db.String(100), db.ForeignKey('staff.email'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('event.event_id'), primary_key=True)
)

assists = db.Table('assists',
    db.Column('staff_email', db.String(100), db.ForeignKey('staff.email'), primary_key=True),
    db.Column('volunteer_email', db.String(100), db.ForeignKey('volunteer.email'), primary_key=True)
)

# ----- Help System -----
class RequestHelp(db.Model):
    __tablename__ = 'request_help'
    request_id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(100), db.ForeignKey('user.email'), nullable=False)
    staff_email = db.Column(db.String(100), db.ForeignKey('staff.email'), nullable=False)
    request_text = db.Column(db.Text, nullable=False)
    response_text = db.Column(db.Text)
    status = db.Column(db.String(50), default='open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)    