# CMPT 354 Library Database Miniproject

## Table of Contents
- [Set Up Instructions](#set-up-instructions)
  - [Step 1: Clone the Repository](#step-1-clone-the-repository)
  - [Step 2: Backend Server Setup](#step-2-backend-server-setup)
  - [Step 3: Frontend Setup](#step-3-frontend-setup)
- [Guide](#guide)
  - [Database Schema](#database-schema)
  - [API Endpoints](#api-endpoints)
  - [Frontend Usage](#frontend-usage)

---

## Set Up Instructions

### Step 1: Clone the Repository
1. Open a terminal and navigate to your desired project directory.
2. Clone the repository using:
   ```bash
   git clone https://github.com/jnn4/CMPT-354-MP.git
   ```
3. Navigate into the project folder:
   ```bash
   cd CMPT-354-MP
   ```

### Step 2: Backend Server Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the database:
   ```bash
   python setup_db.py
   ```
4. Start the backend server:
   ```bash
   python app.py
   ```
   The server should now be running at `http://localhost:5000`.

### Step 3: Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the frontend development server:
   ```bash
   npm start
   ```
   The frontend should now be running at `http://localhost:3000`.

---

## Guide

### Database Schema
The library database consists of the following tables:
- `Books` (book_id, title, author, genre, available_copies)
- `Users` (user_id, name, email, membership_type)
- `Loans` (loan_id, book_id, user_id, issue_date, return_date)

### API Endpoints
- `GET /books` - Retrieve a list of books
- `POST /books` - Add a new book
- `GET /users` - Retrieve a list of users
- `POST /loans` - Issue a book loan
- `GET /loans` - Retrieve active loans

### Frontend Usage
- Browse available books
- Register and log in as a user
- Borrow and return books
- Track loan history

---

This completes the setup and guide for the **CMPT 354 Library Database Miniproject**.

