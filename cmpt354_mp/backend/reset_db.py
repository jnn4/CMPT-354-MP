from app import app, db
import os

def reset_database():
    # Delete the existing database file if it exists
    if os.path.exists('library.db'):
        os.remove('library.db')
        print("Removed existing database file")
    
    # Create all tables
    with app.app_context():
        db.create_all()
        print("Created new database with all tables")

if __name__ == '__main__':
    reset_database() 