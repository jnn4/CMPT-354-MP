from extensions import db

# User model

class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)  # Field for hashed password
    role = db.Column(db.String(50), nullable=False)

    def __init__(self, name, email, password_hash, role): # might be able to delete this later!
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.role = role

    books = db.relationship('Book', backref='user', lazy=True)


# Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year_published = db.Column(db.Integer, nullable=True)
    borrowed = db.Column(db.Boolean, default=False)

    # Foreign key to the User model (many-to-one relationship)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    
    # You can add a backref to access the User who borrowed the book
    # user = db.relationship('User', backref=db.backref('borrowed_books', lazy=True))

# Commented out for now! easier for debugging

# # Event model
# class Events(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.String(200), nullable=False)
#     date = db.Column(db.String(50), nullable=False)
#     rsvp = db.Column(db.Boolean, default=False)

# # Staff model
# class Staff(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     position = db.Column(db.String(100), nullable=False)

# # Volunteer model
# class Volunteer(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     position = db.Column(db.String(100), nullable=False)
