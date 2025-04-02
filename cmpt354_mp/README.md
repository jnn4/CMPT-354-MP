# CMPT 354 Library Management System

A comprehensive library management system built with Flask (backend) and React (frontend) that allows users to manage books, events, staff, volunteers, and more.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Usage](#usage)
  - [User Features](#user-features)
  - [Staff Features](#staff-features)

## Features

### User Features
- User registration and authentication
- Browse and search library items
- View and register for events
- Borrow and return items
- View borrowing history
- Make donations
- Request help from staff
- Volunteer registration

### Staff Features
- Staff authentication
- Manage library items (add, delete, update)
- Manage events (create, delete, update)
- Manage fines
- Manage staff members
- Manage volunteers
- Handle user requests

## Prerequisites
- Python 3.x
- Node.js and npm
- SQLite3

## Setup Instructions

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```bash
   python setup_db.py
   ```

5. Start the backend server:
   ```bash
   python app.py
   ```
   The backend server will run at `http://localhost:8000`

### Frontend Setup
1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the frontend development server:
   ```bash
   npm run dev
   ```
   The frontend will run at `http://localhost:5173`

## Usage

### User Features
1. **Registration and Login**
   - Click "Sign Up" to create a new account
   - Use your email and password to log in

2. **Browsing and Borrowing**
   - View available items in the library
   - Borrow items and view your borrowing history
   - Return items when done

3. **Events**
   - Browse upcoming events
   - Register for events you're interested in
   - View your event registrations

4. **Volunteering**
   - Register as a volunteer
   - View volunteer opportunities
   - Track your volunteer status

### Staff Features
1. **Authentication**
   - Log in with staff credentials
   - Access staff-specific features

2. **Management Features**
   - Manage library items (add, delete, update)
   - Manage events (create, delete, update)
   - Manage fines
   - Manage staff members
   - Manage volunteers
   - Handle user requests

3. **Dashboard**
   - View system overview
   - Monitor user activities
   - Track inventory and events

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/signup` - User registration

### Items
- `GET /items` - Get all items
- `POST /items` - Add new item
- `DELETE /items/<id>` - Delete item

### Events
- `GET /events` - Get all events
- `POST /events` - Create new event
- `DELETE /events/<id>` - Delete event

### Staff
- `GET /staff` - Get all staff members
- `POST /staff` - Add new staff member
- `DELETE /staff/<id>` - Delete staff member

### Volunteers
- `GET /volunteer` - Get all volunteers
- `POST /volunteer` - Add new volunteer
- `DELETE /volunteer/<id>` - Delete volunteer

### Fines
- `GET /fines` - Get all fines
- `POST /fines` - Create new fine
- `DELETE /fines/<id>` - Delete fine

## Database Schema
The system uses SQLite with the following main tables:
- `Person` - Basic user information
- `User` - User accounts and authentication
- `Staff` - Staff member information
- `Volunteer` - Volunteer information
- `Item` - Library items
- `Event` - Library events
- `BorrowTransaction` - Item borrowing records
- `Fines` - Fine records
- `RequestHelp` - User help requests

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

