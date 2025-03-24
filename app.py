from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Route to display the form and handle POST requests to insert user data
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        
        # Check if email already exists in the database
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE email = ?", (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            return f"Error: User with email {email} already exists."
        
        # Insert data into the database
        cursor.execute("INSERT INTO Users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        conn.close()
        
        return f"User {name} added successfully!"
    
    return render_template('add_user.html')

# Route to display all users
@app.route('/')
def index():
    # Fetch all users from the database
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    conn.close()
    
    return render_template('index.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
