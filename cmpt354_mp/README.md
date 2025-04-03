# Running the App Locally

## Prerequisites
Make sure you have the following installed:
- [Python 3.9+](https://www.python.org/downloads/)
- [Node.js and npm](https://nodejs.org/)
- [SQLite](https://www.sqlite.org/)

## Setup Instructions

### 1. **Clone the Repository**

First, make sure you have the project repository on your local machine. You can clone it using Git:

```bash
git clone <repository-url>
cd cmpt354_mp
```

### 2. **Setup the Backend (Flask API)**

#### a. Create a Python Virtual Environment
In the root of the project directory, set up a Python virtual environment. This will allow you to manage project-specific dependencies.

```bash
python3 -m venv venv
```

#### b. Activate the Virtual Environment
Activate the virtual environment. This step may differ based on your operating system:

- **For macOS/Linux:**
    ```bash
    source venv/bin/activate
    ```

- **For Windows (cmd):**
    ```bash
    venv\Scripts\activate
    ```

- **For Windows (PowerShell):**
    ```bash
    .\venv\Scripts\Activate.ps1
    ```

#### c. Install the Required Dependencies
Install the project dependencies using `pip`. The required dependencies are listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3. **Setup the Database**

The backend relies on SQLite to store data, and you need to seed the database with initial data.

#### a. Run the Database Seeding Script
Once you've set up the virtual environment and installed the dependencies, run the following command to seed the database:

```bash
python3 seed_db.py
```

This script will populate your database with initial data.

### 4. **Run the Flask Application (Backend)**

After seeding the database, you can start the Flask API. To do so, run:

```bash
python3 app.py
```

This will start the Flask backend server on `http://localhost:8000`. You should now have the API running locally.

#### Optional: Running the Flask App with a Specific Port
If you want to run it on a different port, you can change the port in `app.py` or specify it when starting the app like this:

```bash
python3 app.py
```

### 5. **Setup the Frontend (React App)**

#### a. Install Frontend Dependencies
Next, set up the React frontend, which will communicate with the Flask API. You need to install the necessary Node.js dependencies.

1. Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```

2. Install the dependencies using npm (make sure you're in the `frontend` directory):

    ```bash
    npm install
    ```

#### b. Run the React Development Server
Once the dependencies are installed, run the development server for the frontend:

```bash
npm run dev
```

The React app should now be running on `http://localhost:5173` by default.

---

## Full Workflow

To summarize the steps, here is the full workflow to run your app locally:

```bash
# 1. Clone the repo and navigate to the project folder
git clone <repository-url>
cd cmpt354_mp

# 2. Set up the Python virtual environment
python3 -m venv venv
source venv/bin/activate   # For macOS/Linux
# venv\Scripts\activate    # For Windows (cmd)

# 3. Install the required Python dependencies
pip install -r requirements.txt

# 4. Seed the database with initial data
python3 seed_db.py

# 5. Start the Flask API backend
python3 app.py

# 6. Set up the frontend (React app)
cd frontend
npm install

# 7. Run the React development server
npm run dev
```

### 6. **Testing the App Locally**

After following these steps, you should be able to access:

- The **backend API**: [http://localhost:8000](http://localhost:8000)
- The **frontend**: [http://localhost:5173](http://localhost:5173)

### 7. **Troubleshooting**

- **Virtual Environment Issues**: If you encounter issues with the virtual environment not activating, make sure to use the correct command for your operating system.
- **Port Conflicts**: If the default port (`8000` for Flask and `5173` for React) is already in use, you can change the port in both `app.py` (Flask) and `vite.config.js` (React).

---

## Additional Information

- **Frontend**: The frontend is built using **React** with **Vite**. The React app communicates with the Flask backend via HTTP requests.
  
- **Backend**: The backend is built using **Flask** and uses **SQLite** for data storage. The app provides various RESTful API endpoints, which can be accessed by the frontend.

---
