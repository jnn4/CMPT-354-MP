from datetime import datetime, timedelta, date
from werkzeug.security import generate_password_hash
from flask import Flask
from extensions import db
from models import (
    Person, User, Staff, Volunteer, Item, 
    FutureItem, BorrowTransaction, Fine, 
    Room, Event, RequestHelp
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Realistic names dataset
FIRST_NAMES = [
    'Emma', 'Liam', 'Olivia', 'Noah', 'Ava',
    'William', 'Sophia', 'James', 'Isabella', 'Benjamin'
]

LAST_NAMES = [
    'Smith', 'Johnson', 'Williams', 'Brown', 'Jones',
    'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez'
]

BOOK_TITLES = [
    ('To Kill a Mockingbird', 'Harper Lee', 1960),
    ('1984', 'George Orwell', 1949),
    ('The Great Gatsby', 'F. Scott Fitzgerald', 1925),
    ('Pride and Prejudice', 'Jane Austen', 1813),
    ('The Catcher in the Rye', 'J.D. Salinger', 1951),
    ('The Hobbit', 'J.R.R. Tolkien', 1937),
    ('Fahrenheit 451', 'Ray Bradbury', 1953),
    ('Moby-Dick', 'Herman Melville', 1851),
    ('The Diary of a Young Girl', 'Anne Frank', 1947),
    ('The Alchemist', 'Paulo Coelho', 1988)
]

MEDIA_ITEMS = [
    ('Abbey Road', 'The Beatles', 1969, 'cd'),
    ('Thriller', 'Michael Jackson', 1982, 'cd'),
    ('Dark Side of the Moon', 'Pink Floyd', 1973, 'cd'),
    ('National Geographic: Wildlife', 'Various', 2024, 'magazine'),
    ('Scientific American: AI Special', 'Editors', 2024, 'journal'),
    ('Python Programming Weekly', 'Tech Publications', 2024, 'magazine'),
    ('The Lord of the Rings Audiobook', 'J.R.R. Tolkien', 1954, 'audiobook'),
    ('Cosmos: A Spacetime Odyssey', 'Carl Sagan', 2014, 'dvd'),
    ('The Art of Computer Programming', 'Donald Knuth', 1968, 'reference'),
    ('World History Encyclopedia', 'Various Authors', 2020, 'reference')
]

def create_people():
    people = []
    for i in range(10):
        people.append(Person(
            email=f'{FIRST_NAMES[i].lower()}.{LAST_NAMES[i].lower()}@example.com',
            first_name=FIRST_NAMES[i],
            last_name=LAST_NAMES[i],
            phone_num=f'555-01{i:02}',
            age=random.randint(18, 65)
        ))
    db.session.bulk_save_objects(people)
    db.session.commit()

def create_users():
    users = []
    for i in range(10):
        users.append(User(
            email=f'{FIRST_NAMES[i].lower()}.{LAST_NAMES[i].lower()}@example.com',
            password_hash=generate_password_hash(f'{FIRST_NAMES[i]}2025!', method="pbkdf2:sha256")
        ))
    db.session.bulk_save_objects(users)
    db.session.commit()

def create_staff():
    staff = [
        Staff(email='emma.smith@example.com', wage=22.50),
        Staff(email='liam.johnson@example.com', wage=20.00),
        Staff(email='olivia.williams@example.com', wage=19.50)
    ]
    db.session.bulk_save_objects(staff)
    db.session.commit()

def create_volunteers():
    volunteers = [
        Volunteer(email='noah.brown@example.com', start_date=date(2024, 1, 15), end_date=date(2025, 1, 14)),
        Volunteer(email='ava.jones@example.com', start_date=date(2025, 3, 1), end_date=None),
        Volunteer(email='william.garcia@example.com', start_date=date(2025, 2, 1), end_date=None)
    ]
    db.session.bulk_save_objects(volunteers)
    db.session.commit()

def create_items():
    items = []
    # Add books
    for title, author, year in BOOK_TITLES:
        items.append(Item(
            title=title,
            author=author,
            pub_year=year,
            type='book',
            status='available' if random.random() > 0.2 else 'borrowed'
        ))
    
    # Add media items
    for title, author, year, media_type in MEDIA_ITEMS:
        items.append(Item(
            title=title,
            author=author,
            pub_year=year,
            type=media_type,
            status='available' if random.random() > 0.3 else 'borrowed'
        ))
    
    db.session.bulk_save_objects(items)
    db.session.commit()

def create_borrow_transactions():
    transactions = []
    for i in range(1, 11):
        borrow_date = datetime.now() - timedelta(days=random.randint(1, 30))
        transactions.append(BorrowTransaction(
            user_email=f'{FIRST_NAMES[i-1].lower()}.{LAST_NAMES[i-1].lower()}@example.com',
            item_id=i,
            borrow_date=borrow_date,
            due_date=borrow_date + timedelta(days=14),
            return_date=borrow_date + timedelta(days=random.randint(0, 14)) if random.random() > 0.4 else None
        ))
    db.session.bulk_save_objects(transactions)
    db.session.commit()

def create_fines():
    fines = []
    for i in range(1, 6):  # Only 5 overdue items
        fines.append(Fine(
            trans_id=i,
            amount=random.uniform(5.0, 25.0),
            paid=random.choice([True, False])
        ))
    db.session.bulk_save_objects(fines)
    db.session.commit()

def create_rooms():
    rooms = [
        Room(name='Main Reading Room', capacity=120),
        Room(name='Children\'s Story Corner', capacity=30),
        Room(name='Silent Study Area', capacity=40),
        Room(name='Multimedia Lab', capacity=25),
        Room(name='Conference Room A', capacity=20),
        Room(name='Local History Archive', capacity=15),
        Room(name='Creative Writing Space', capacity=18),
        Room(name='Tech Innovation Hub', capacity=20),
        Room(name='Genealogy Research Room', capacity=12),
        Room(name='Community Meeting Room', capacity=50)
    ]
    db.session.bulk_save_objects(rooms)
    db.session.commit()

def create_events():
    events = [
        Event(
            name='Python Programming Workshop',
            type='workshop',
            date=date(2025, 4, 15),
            time=datetime.strptime('14:00', '%H:%M').time(),
            room_id=8,
            audience_type='adults'
        ),
        Event(
            name='Children\'s Story Hour',
            type='storytelling',
            date=date(2025, 4, 16),
            time=datetime.strptime('10:30', '%H:%M').time(),
            room_id=2,
            audience_type='children'
        ),
        Event(
            name='Local Author Showcase',
            type='meetup',
            date=date(2025, 4, 18),
            time=datetime.strptime('18:00', '%H:%M').time(),
            room_id=10,
            audience_type='all ages'
        )
    ]
    db.session.bulk_save_objects(events)
    db.session.commit()

def create_help_requests():
    requests = [
        RequestHelp(
            user_email='emma.smith@example.com',
            request_text='Need help locating historical archives for local research project',
            status=True
        ),
        RequestHelp(
            user_email='liam.johnson@example.com',
            request_text='Looking for recommendations on Python programming resources',
            status=False
        ),
        RequestHelp(
            user_email='olivia.williams@example.com',
            request_text='Assistance needed with ebook platform access',
            status=True
        )
    ]
    db.session.bulk_save_objects(requests)
    db.session.commit()

def insert_data():
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        create_people()
        create_users()
        create_staff()
        create_volunteers()
        create_items()
        create_borrow_transactions()
        create_fines()
        create_rooms()
        create_events()
        create_help_requests()

        print("Successfully created realistic library dataset!")

if __name__ == "__main__":
    import random
    insert_data()
