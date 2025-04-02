import sqlite3

# Initialize Database Connection
def create_connection():
    conn = sqlite3.connect("library.db")
    return conn

# Create Tables if they do not exist
def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    # Create Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
    """)

    # Create Items table (Books, CDs, etc.)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        type TEXT NOT NULL,  -- e.g., Book, Magazine, CD, etc.
        status TEXT DEFAULT 'available'
    )
    """)

    # Create Borrow Transactions table
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

    # Create Events table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Events (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        date DATETIME,
        location TEXT
    )
    """)

    # Create Attendees table (Users registered for Events)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Attendees (
        user_id INTEGER,
        event_id INTEGER,
        PRIMARY KEY (user_id, event_id),
        FOREIGN KEY(user_id) REFERENCES Users(user_id),
        FOREIGN KEY(event_id) REFERENCES Events(event_id)
    )
    """)

    conn.commit()
    conn.close()

# Populate the tables with initial data
def populate_data():
    conn = create_connection()
    cursor = conn.cursor()

    # Insert Users
    users = [
        ("Alice Johnson", "alice@example.com"),
        ("Bob Smith", "bob@example.com"),
        ("Charlie Brown", "charlie@example.com")
    ]
    cursor.executemany("INSERT OR IGNORE INTO Users (name, email) VALUES (?, ?)", users)

    # Insert Items
    items = [
        ("The Great Gatsby", "Book"),
        ("National Geographic", "Magazine"),
        ("Thriller - Michael Jackson", "CD"),
        ("To Kill a Mockingbird", "Book"),
        ("Scientific American", "Magazine")
    ]
    cursor.executemany("INSERT OR IGNORE INTO Items (title, type) VALUES (?, ?)", items)

    # Insert Borrow Transactions
    cursor.execute("SELECT user_id FROM Users WHERE name = 'Alice Johnson'")
    alice_id = cursor.fetchone()[0]

    cursor.execute("SELECT user_id FROM Users WHERE name = 'Bob Smith'")
    bob_id = cursor.fetchone()[0]

    cursor.execute("SELECT item_id FROM Items WHERE title = 'The Great Gatsby'")
    gatsby_id = cursor.fetchone()[0]

    cursor.execute("SELECT item_id FROM Items WHERE title = 'Thriller - Michael Jackson'")
    thriller_id = cursor.fetchone()[0]

    borrow_transactions = [
        (alice_id, gatsby_id),
        (bob_id, thriller_id)
    ]
    cursor.executemany("""
    INSERT OR IGNORE INTO BorrowTransactions (user_id, item_id, due_date)
    VALUES (?, ?, DATE(CURRENT_TIMESTAMP, '+14 days'))
    """, borrow_transactions)

    # Mark borrowed items as 'borrowed'
    cursor.execute("UPDATE Items SET status = 'borrowed' WHERE item_id = ?", (gatsby_id,))
    cursor.execute("UPDATE Items SET status = 'borrowed' WHERE item_id = ?", (thriller_id,))

    # Insert Events
    events = [
        ("Book Reading: Classic Literature", "2025-04-15", "Library Hall A"),
        ("Music Night: Retro Hits", "2025-05-20", "Library Auditorium")
    ]
    cursor.executemany("INSERT OR IGNORE INTO Events (name, date, location) VALUES (?, ?, ?)", events)

    # Insert Attendees
    cursor.execute("SELECT event_id FROM Events WHERE name = 'Book Reading: Classic Literature'")
    book_event_id = cursor.fetchone()[0]

    cursor.execute("SELECT event_id FROM Events WHERE name = 'Music Night: Retro Hits'")
    music_event_id = cursor.fetchone()[0]

    attendees = [
        (alice_id, book_event_id),
        (bob_id, music_event_id)
    ]
    cursor.executemany("INSERT OR IGNORE INTO Attendees (user_id, event_id) VALUES (?, ?)", attendees)

    conn.commit()
    conn.close()

# Display all users
def show_users():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    print("\nUsers:")
    for user in users:
        print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")
    conn.close()

# Display all items
def show_items():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Items")
    items = cursor.fetchall()
    print("\nLibrary Items:")
    for item in items:
        print(f"ID: {item[0]}, Title: {item[1]}, Type: {item[2]}, Status: {item[3]}")
    conn.close()

# Display all events
def show_events():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Events")
    events = cursor.fetchall()
    print("\nEvents:")
    for event in events:
        print(f"ID: {event[0]}, Name: {event[1]}, Date: {event[2]}, Location: {event[3]}")
    conn.close()

# Show main menu
def show_menu():
    print("\nLibrary System Menu:")
    print("1. Show Users")
    print("2. Show Items")
    print("3. Show Events")
    print("4. Exit")

# Main Function
def main():
    create_tables()
    populate_data()
    
    while True:
        show_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            show_users()
        elif choice == '2':
            show_items()
        elif choice == '3':
            show_events()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
