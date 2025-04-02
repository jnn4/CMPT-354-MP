# from flask import Blueprint, request, jsonify
# from models import User, db
# from werkzeug.security import generate_password_hash, check_password_hash
# from sqlalchemy.exc import IntegrityError

# user_bp = Blueprint('user', __name__, url_prefix='/users')

# # Create a new user
# @user_bp.route('/', methods=['POST'])
# def create_user():
#     try:
#         data = request.get_json()

#         username = data.get('username')
#         email = data.get('email')
#         password = data.get('password')
#         role = data.get('role', 'user')  # Default role is 'user'

#         # Validation
#         if not username or not email or not password:
#             return jsonify({"message": "Username, Email, and Password are required!"}), 400

#         # Check if the username or email already exists
#         existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
#         if existing_user:
#             return jsonify({"message": "Username or Email already exists!"}), 400

#         # Hash the password
#         hashed_password = generate_password_hash(password)

#         # Create new user
#         new_user = User(username=username, email=email, password=hashed_password, role=role)
#         db.session.add(new_user)
#         db.session.commit()

#         return jsonify({
#             "message": "User created successfully!",
#             "user_id": new_user.id,
#             "username": new_user.username,
#             "email": new_user.email,
#             "role": new_user.role
#         }), 201

#     except IntegrityError:
#         db.session.rollback()
#         return jsonify({"message": "A database error occurred!"}), 500
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"message": str(e)}), 500

# # User login
# @user_bp.route('/login', methods=['POST'])
# def login_user():
#     try:
#         data = request.get_json()

#         email = data.get('email')
#         password = data.get('password')

#         # Validation
#         if not email or not password:
#             return jsonify({"message": "Email and Password are required!"}), 400

#         user = User.query.filter_by(email=email).first()
#         if not user or not check_password_hash(user.password, password):
#             return jsonify({"message": "Invalid credentials!"}), 401

#         return jsonify({
#             "message": "Login successful!",
#             "user_id": user.id,
#             "username": user.username,
#             "email": user.email,
#             "role": user.role
#         }), 200

#     except Exception as e:
#         return jsonify({"message": str(e)}), 500

# Get user by ID
@user_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found!"}), 404

#         return jsonify({
#             "user_id": user.id,
#             "username": user.username,
#             "email": user.email,
#             "role": user.role
#         }), 200

#     except Exception as e:
#         return jsonify({"message": str(e)}), 500

# Update user details
@user_bp.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()
        user = User.query.get(user_id)

#         if not user:
#             return jsonify({"message": "User not found!"}), 404

#         username = data.get('username', user.username)
#         email = data.get('email', user.email)
#         password = data.get('password', user.password)
#         role = data.get('role', user.role)

#         # Hash the password if it was updated
#         if password != user.password:
#             password = generate_password_hash(password)

#         # Update user fields
#         user.username = username
#         user.email = email
#         user.password = password
#         user.role = role

#         db.session.commit()

#         return jsonify({
#             "message": "User updated successfully!",
#             "user_id": user.id,
#             "username": user.username,
#             "email": user.email,
#             "role": user.role
#         }), 200

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"message": str(e)}), 500

# Delete user by ID
@user_bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)

#         if not user:
#             return jsonify({"message": "User not found!"}), 404

#         db.session.delete(user)
#         db.session.commit()

#         return jsonify({"message": "User deleted successfully!"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

# Populate the database with users
@user_bp.route('/user/populate_user', methods=['POST'])
def populate_user():
    try:
        user_data = [
            {"user_id": 1, "email": "alice@example.com", "password": generate_password_hash("password123")},
            {"user_id": 2, "email": "bob@example.com", "password": generate_password_hash("securePass1")},
            {"user_id": 3, "email": "charlie@example.com", "password": generate_password_hash("helloWorld!")},
            {"user_id": 4, "email": "dave@example.com", "password": generate_password_hash("myPassword42")},
            {"user_id": 5, "email": "eve@example.com", "password": generate_password_hash("superSecret")},
            {"user_id": 6, "email": "frank@example.com", "password": generate_password_hash("passw0rd!")},
            {"user_id": 7, "email": "grace@example.com", "password": generate_password_hash("admin123")},
            {"user_id": 8, "email": "heidi@example.com", "password": generate_password_hash("letMeIn!")},
            {"user_id": 9, "email": "ivan@example.com", "password": generate_password_hash("qwerty987")},
            {"user_id": 10, "email": "judy@example.com", "password": generate_password_hash("trustNo1!")}
        ]

        for user_data in user_data:
            user = User(**user_data)
            db.session.add(user)

        db.session.commit();
        return jsonify({"message": "User populated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to populate users", "error": str(e)}), 500