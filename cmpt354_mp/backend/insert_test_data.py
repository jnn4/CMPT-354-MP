from app import app, db
from models import Person, User, Item, BorrowTransaction

def insert_test_data():
    with app.app_context():
        # Clear existing data (optional)
        db.session.query(BorrowTransaction).delete()
        db.session.query(Item).delete()
        db.session.query(User).delete()
        db.session.query(Person).delete()

        # Create test users
        person1 = Person(
            email="user1@example.com",
            first_name="Johnny",
            last_name="Doe",
            age=25
        )
        user1 = User(
            email=person1.email,
            password_hash="pbkdf2:sha256:260000$..."  # Use generate_password_hash() here
        )

        person2 = Person(
            email="user2@example.com",
            first_name="John",
            last_name="Smith",
            age=30
        )
        user2 = User(
            email=person2.email,
            password_hash="pbkdf2:sha256:260000$..."  # Use generate_password_hash() here
        )

        # Create test items
        items = [
            Item(
                title="The Great Gatsby",
                author="F. Scott Fitzgerald",
                pub_year=1925,
                type="book",
                status="available"
            ),
            Item(
                title="National Geographic",
                author="Various Authors",
                pub_year=2023,
                type="magazine",
                status="available"
            ),
            Item(
                title="Abbey Road",
                author="The Beatles",
                pub_year=1969,
                type="cd",
                status="available"
            )
        ]

        # Add all to session
        db.session.add_all([person1, user1, person2, user2] + items)
        
        try:
            db.session.commit()
            print("Test data inserted successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error inserting test data: {str(e)}")

if __name__ == '__main__':
    insert_test_data()
