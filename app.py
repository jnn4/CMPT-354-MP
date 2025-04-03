import sqlite3
import random
from datetime import datetime, timedelta

def create_connection():
    return sqlite3.connect("library.db")

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        type TEXT NOT NULL,
        status TEXT DEFAULT 'available',
        is_future_item BOOLEAN DEFAULT 0
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS BorrowTransactions (
        trans_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        borrowed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        due_date DATETIME,
        return_date DATETIME,
        FOREIGN KEY(user_id) REFERENCES Users(user_id),
        FOREIGN KEY(item_id) REFERENCES Items(item_id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Fines (
        fine_id INTEGER PRIMARY KEY AUTOINCREMENT,
        trans_id INTEGER NOT NULL,
        amount DECIMAL(10,2) NOT NULL,
        status TEXT DEFAULT 'pending',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        paid_at DATETIME,
        FOREIGN KEY(trans_id) REFERENCES BorrowTransactions(trans_id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Events (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        date DATETIME,
        location TEXT,
        recommended_audience TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Personnel (
        personnel_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        role TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        hire_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'active'
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Volunteers (
        volunteer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        role TEXT,
        FOREIGN KEY(user_id) REFERENCES Users(user_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Attendees (
        attendee_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        event_id INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES Users(user_id),
        FOREIGN KEY(event_id) REFERENCES Events(event_id)
    )
    """)
    
    conn.commit()
    conn.close()

def find_item():
    conn = create_connection()
    cursor = conn.cursor()
    title = input("Enter item title to search: ")
    cursor.execute("SELECT * FROM Items WHERE title LIKE ?", (f"%{title}%",))
    items = cursor.fetchall()
    if items:
        for item in items:
            print(f"ID: {item[0]}, Title: {item[1]}, Type: {item[2]}, Status: {item[3]}")
    else:
        print("No items found.")
    conn.close()

def borrow_item():
    conn = create_connection()
    cursor = conn.cursor()
    
    # List all available items
    cursor.execute("SELECT item_id, title, type FROM Items WHERE status = 'available'")
    available_items = cursor.fetchall()
    
    if available_items:
        print("Available Items to Borrow:")
        for item in available_items:
            print(f"ID: {item[0]}, Title: {item[1]}, Type: {item[2]}")
        
        # Allow user to borrow by typing the title
        title = input("Enter the title of the item you want to borrow: ")
        cursor.execute("SELECT item_id, title, status FROM Items WHERE title LIKE ? AND status = 'available'", (f"%{title}%",))
        item = cursor.fetchone()
        
        if item:
            item_id = item[0]
            user_id = input("Enter your User ID: ")

            cursor.execute("""
            INSERT INTO BorrowTransactions (user_id, item_id, due_date)
            VALUES (?, ?, DATE(CURRENT_TIMESTAMP, '+14 days'))
            """, (user_id, item_id))
            cursor.execute("UPDATE Items SET status = 'borrowed' WHERE item_id = ?", (item_id,))
            conn.commit()
            print(f"Item '{item[1]}' borrowed successfully!")
        else:
            print("No available items found with that title.")
    else:
        print("No items are available to borrow at the moment.")
    
    conn.close()


def return_item():
    conn = create_connection()
    cursor = conn.cursor()
    
    user_id = input("Enter your User ID: ")
    item_id = input("Enter Item ID to return: ")
    
    # Check if the item exists and is currently borrowed by this user
    cursor.execute("""
        SELECT i.title, bt.borrowed_at, bt.due_date, bt.trans_id
        FROM Items i
        JOIN BorrowTransactions bt ON i.item_id = bt.item_id
        WHERE i.item_id = ? AND bt.user_id = ? AND bt.return_date IS NULL
    """, (item_id, user_id))
    
    item = cursor.fetchone()

    if item:
        # Check if the item is overdue
        due_date = datetime.strptime(item[2], '%Y-%m-%d')
        if datetime.now() > due_date:
            print(f"Warning: This item is overdue! It was due on {item[2]}")
            fine_amount = calculate_fine(item[3])
            print(f"A fine of ${fine_amount} has been applied for late return.")
        
        cursor.execute("UPDATE BorrowTransactions SET return_date = CURRENT_TIMESTAMP WHERE item_id = ? AND user_id = ? AND return_date IS NULL", (item_id, user_id))
        cursor.execute("UPDATE Items SET status = 'available' WHERE item_id = ?", (item_id,))
        conn.commit()
        print(f"You have successfully returned: {item[0]}")
        print(f"Borrowed on: {item[1]}")
    else:
        print("Error: Either the item doesn't exist, wasn't borrowed by you, or has already been returned.")

    conn.close()

def donate_item():
    conn = create_connection()
    cursor = conn.cursor()
    title = input("Enter item title: ")
    type_ = input("Enter item type: ")
    cursor.execute("INSERT INTO Items (title, type) VALUES (?, ?)", (title, type_))
    conn.commit()
    print("Thank you for your donation!")
    conn.close()

def find_event():
    conn = create_connection()
    cursor = conn.cursor()
    name = input("Enter event name to search: ")
    cursor.execute("""
        SELECT event_id, name, date, location, recommended_audience 
        FROM Events 
        WHERE name LIKE ?
    """, (f"%{name}%",))
    events = cursor.fetchall()
    if events:
        for event in events:
            print(f"ID: {event[0]}, Name: {event[1]}, Date: {event[2]}, Location: {event[3]}")
            print(f"Recommended Audience: {event[4]}")
            print("-" * 50)
    else:
        print("No events found.")
    conn.close()

def volunteer():
    conn = create_connection()
    cursor = conn.cursor()
    user_id = input("Enter your User ID: ")
    role = input("Enter your preferred volunteer role: ")
    cursor.execute("INSERT INTO Volunteers (user_id, role) VALUES (?, ?)", (user_id, role))
    conn.commit()
    print("Thank you for volunteering!")
    conn.close()

def ask_librarian():
    print("Please visit the help desk or email help@library.com")

def populate_data():
    conn = create_connection()
    cursor = conn.cursor()
    
    # Check if the Users table already has data
    cursor.execute("SELECT COUNT(*) FROM Users")
    user_count = cursor.fetchone()[0]
    
    # Only populate data if Users table is empty
    if user_count == 0:
        # Populate Users
        users = [
            ("Alice Johnson", "alice@example.com"),
            ("Bob Smith", "bob@example.com"),
            ("Charlie Brown", "charlie@example.com"),
            ("Diana Prince", "diana@example.com"),
            ("Eve Adams", "eve@example.com"),
            ("Frank Castle", "frank@example.com"),
            ("Grace Kelly", "grace@example.com"),
            ("Henry Ford", "henry@example.com"),
            ("Ivy Green", "ivy@example.com"),
            ("Jack Ryan", "jack@example.com")
        ]
        cursor.executemany("INSERT OR IGNORE INTO Users (name, email) VALUES (?, ?)", users)
        
        # Populate Items (including future items)
        items = [
            ("The Great Gatsby", "Book", 0),
            ("National Geographic", "Magazine", 0),
            ("Thriller - Michael Jackson", "CD", 0),
            ("To Kill a Mockingbird", "Book", 0),
            ("Scientific American", "Journal", 0),
            ("Harry Potter and the Sorcerer's Stone", "Book", 0),
            ("Time Magazine", "Magazine", 0),
            ("The Beatles - Abbey Road", "CD", 0),
            ("The Art of War", "Book", 0),
            ("Physics Today", "Journal", 0),
            # Future items
            ("Upcoming: The New Science Journal", "Journal", 1),
            ("Upcoming: Modern Art Collection", "Book", 1),
            ("Upcoming: Classical Music Collection", "CD", 1)
        ]
        cursor.executemany("INSERT OR IGNORE INTO Items (title, type, is_future_item) VALUES (?, ?, ?)", items)
        
        # Populate Personnel
        personnel = [
            ("Sarah Wilson", "Head Librarian", "sarah.wilson@library.com"),
            ("Michael Chen", "Reference Librarian", "michael.chen@library.com"),
            ("Emily Rodriguez", "Children's Librarian", "emily.rodriguez@library.com"),
            ("David Thompson", "Technical Services", "david.thompson@library.com"),
            ("Lisa Anderson", "Event Coordinator", "lisa.anderson@library.com")
        ]
        cursor.executemany("INSERT OR IGNORE INTO Personnel (name, role, email) VALUES (?, ?, ?)", personnel)
        
        # Get IDs for relationships
        cursor.execute("SELECT user_id FROM Users")
        user_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT item_id FROM Items")
        item_ids = [row[0] for row in cursor.fetchall()]
        
        # Populate BorrowTransactions (including some overdue ones)
        borrow_transactions = []
        for _ in range(10):
            user_id = random.choice(user_ids)
            item_id = random.choice(item_ids)
            borrowed_at = datetime.now() - timedelta(days=random.randint(1, 30))
            due_date = borrowed_at + timedelta(days=14)
            # Make some transactions overdue
            if random.random() < 0.3:  # 30% chance of being overdue
                return_date = due_date + timedelta(days=random.randint(1, 10))
            else:
                return_date = borrowed_at + timedelta(days=random.randint(1, 13))
            
            borrow_transactions.append((
                user_id, 
                item_id, 
                borrowed_at.strftime('%Y-%m-%d %H:%M:%S'),
                due_date.strftime('%Y-%m-%d'),
                return_date.strftime('%Y-%m-%d %H:%M:%S') if return_date <= datetime.now() else None
            ))
        
        cursor.executemany("""
            INSERT OR IGNORE INTO BorrowTransactions 
            (user_id, item_id, borrowed_at, due_date, return_date)
            VALUES (?, ?, ?, ?, ?)
        """, borrow_transactions)
        
        # Populate Fines for overdue returns
        cursor.execute("""
            SELECT trans_id, due_date, return_date
            FROM BorrowTransactions
            WHERE return_date > due_date
        """)
        overdue_transactions = cursor.fetchall()
        
        for trans in overdue_transactions:
            trans_id, due_date, return_date = trans
            due_date = datetime.strptime(due_date, '%Y-%m-%d')
            return_date = datetime.strptime(return_date, '%Y-%m-%d %H:%M:%S')
            days_overdue = (return_date - due_date).days
            fine_amount = days_overdue  # $1 per day
            
            cursor.execute("""
                INSERT OR IGNORE INTO Fines (trans_id, amount, status, paid_at)
                VALUES (?, ?, ?, ?)
            """, (
                trans_id,
                fine_amount,
                'paid' if random.random() < 0.7 else 'pending',  # 70% chance of being paid
                datetime.now().strftime('%Y-%m-%d %H:%M:%S') if random.random() < 0.7 else None
            ))
        
        # Populate Events with recommended audiences
        events = [
            ("Book Reading: Classic Literature", "2025-04-15", "Library Hall A", "Adults"),
            ("Music Night: Retro Hits", "2025-05-20", "Library Auditorium", "All Ages"),
            ("Science & Tech Talk", "2025-06-10", "Main Conference Room", "Teens and Adults"),
            ("Art Exhibition: Modern Art", "2025-07-25", "Art Room 1", "All Ages"),
            ("Film Screening: Sci-Fi Classics", "2025-08-30", "Screening Room", "Teens and Adults"),
            ("Poetry Night", "2025-09-12", "Library Café", "Adults"),
            ("Childrens Story Time", "2025-10-05", "Kids Section", "Children (5-12)"),
            ("History Talk: Ancient Civilizations", "2025-11-20", "Library Hall B", "Teens and Adults"),
            ("Coding Workshop", "2025-12-15", "Computer Lab", "Teens"),
            ("Holiday Book Fair", "2026-01-05", "Main Lobby", "All Ages")
        ]
        cursor.executemany("""
            INSERT OR IGNORE INTO Events 
            (name, date, location, recommended_audience)
            VALUES (?, ?, ?, ?)
        """, events)
        
        # Populate Volunteers
        volunteer_roles = ["Event Assistant", "Book Shelver", "Reading Tutor", "Tech Helper", "Event Coordinator"]
        volunteers = [
            (random.choice(user_ids), random.choice(volunteer_roles))
            for _ in range(5)
        ]
        cursor.executemany("INSERT OR IGNORE INTO Volunteers (user_id, role) VALUES (?, ?)", volunteers)
        
        # Populate Attendees
        cursor.execute("SELECT event_id FROM Events")
        event_ids = [row[0] for row in cursor.fetchall()]
        
        attendees = [
            (random.choice(user_ids), random.choice(event_ids))
            for _ in range(15)
        ]
        cursor.executemany("INSERT OR IGNORE INTO Attendees (user_id, event_id) VALUES (?, ?)", attendees)
        
        conn.commit()
        print("Database populated with sample data.")
    else:
        print("Database already populated. Skipping data population.")
    
    conn.close()

def register_for_event():
    conn = create_connection()
    cursor = conn.cursor()

    # Display available events
    cursor.execute("SELECT event_id, name, date, location FROM Events")
    events = cursor.fetchall()

    if events:
        print("Available Events:")
        for event in events:
            print(f"ID: {event[0]}, Name: {event[1]}, Date: {event[2]}, Location: {event[3]}")
        
        # Ask the user to select an event
        event_id = input("Enter the Event ID to register for: ")
        user_id = input("Enter your User ID: ")

        # Check if the user is already registered
        cursor.execute("SELECT * FROM Attendees WHERE user_id = ? AND event_id = ?", (user_id, event_id))
        if cursor.fetchone():
            print("You are already registered for this event.")
        else:
            # Register the user for the event
            cursor.execute("INSERT INTO Attendees (user_id, event_id) VALUES (?, ?)", (user_id, event_id))
            conn.commit()
            print("You have successfully registered for the event!")
    else:
        print("No events available to register for.")

    conn.close()

def calculate_fine(trans_id):
    conn = create_connection()
    cursor = conn.cursor()
    
    # Get transaction details
    cursor.execute("""
        SELECT borrowed_at, due_date, return_date
        FROM BorrowTransactions
        WHERE trans_id = ?
    """, (trans_id,))
    
    trans = cursor.fetchone()
    if not trans:
        return 0
    
    borrowed_at = datetime.strptime(trans[0], '%Y-%m-%d %H:%M:%S')
    due_date = datetime.strptime(trans[1], '%Y-%m-%d')
    return_date = datetime.strptime(trans[2], '%Y-%m-%d %H:%M:%S') if trans[2] else datetime.now()
    
    # Calculate days overdue
    days_overdue = (return_date - due_date).days
    if days_overdue <= 0:
        return 0
    
    # Fine rate: $1 per day overdue
    fine_amount = days_overdue
    
    # Create fine record
    cursor.execute("""
        INSERT INTO Fines (trans_id, amount)
        VALUES (?, ?)
    """, (trans_id, fine_amount))
    
    conn.commit()
    conn.close()
    return fine_amount

def add_personnel():
    conn = create_connection()
    cursor = conn.cursor()
    
    name = input("Enter personnel name: ")
    role = input("Enter role: ")
    email = input("Enter email: ")
    
    cursor.execute("""
        INSERT INTO Personnel (name, role, email)
        VALUES (?, ?, ?)
    """, (name, role, email))
    
    conn.commit()
    print("Personnel added successfully!")
    conn.close()

def add_future_item():
    conn = create_connection()
    cursor = conn.cursor()
    
    title = input("Enter item title: ")
    type_ = input("Enter item type: ")
    
    cursor.execute("""
        INSERT INTO Items (title, type, is_future_item)
        VALUES (?, ?, 1)
    """, (title, type_))
    
    conn.commit()
    print("Future item added successfully!")
    conn.close()

def view_user_fines():
    conn = create_connection()
    cursor = conn.cursor()
    
    user_id = input("Enter your User ID: ")
    
    # Get all fines for the user through their transactions
    cursor.execute("""
        SELECT f.fine_id, i.title, f.amount, f.status, f.created_at, f.paid_at
        FROM Fines f
        JOIN BorrowTransactions bt ON f.trans_id = bt.trans_id
        JOIN Items i ON bt.item_id = i.item_id
        WHERE bt.user_id = ?
        ORDER BY f.created_at DESC
    """, (user_id,))
    
    fines = cursor.fetchall()
    
    if fines:
        print("\nYour Fines:")
        print("-" * 50)
        total_pending = 0
        for fine in fines:
            print(f"Fine ID: {fine[0]}")
            print(f"Item: {fine[1]}")
            print(f"Amount: ${fine[2]}")
            print(f"Status: {fine[3]}")
            print(f"Created: {fine[4]}")
            if fine[5]:  # paid_at
                print(f"Paid: {fine[5]}")
            if fine[3] == 'pending':
                total_pending += fine[2]
            print("-" * 50)
        print(f"Total Pending Fines: ${total_pending}")
    else:
        print("No fines found for this user.")
    
    conn.close()

def show_menu():
    print("\nLibrary System Menu:")
    print("1. Find an Item")
    print("2. Borrow an Item")
    print("3. Return an Item")
    print("4. Donate an Item")
    print("5. Find an Event")
    print("6. Register For an Event")
    print("7. Volunteer for the Library")
    print("8. Ask a Librarian")
    print("9. Add Personnel")
    print("10. Add Future Item")
    print("11. View Your Fines")
    print("12. Exit")

def main():
    create_tables()
    populate_data()
    print("Database populated with sample data.")

    while True:
        show_menu()
        choice = input("Enter your choice: ")
        if choice == '1':
            find_item()
        elif choice == '2':
            borrow_item()
        elif choice == '3':
            return_item()
        elif choice == '4':
            donate_item()
        elif choice == '5':
            find_event()
        elif choice == '6':
            register_for_event()
        elif choice == '7':
            volunteer()
        elif choice == '8':
            ask_librarian()
        elif choice == '9':
            add_personnel()
        elif choice == '10':
            add_future_item()
        elif choice == '11':
            view_user_fines()
        elif choice == '12':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
