from app.models.basemodel import BaseModel
import re
from sqlalchemy.orm import validates
from app import bcrypt
from app import db

class User(BaseModel, db.Model):
    """User model representing application users."""
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


    @validates('email')
    def validate_email(self, key, email):
        """Validate email format before saving."""
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email address format.")
        return email

    @validates('password')
    def validate_password(self, key, password):
        """Ensure password meets length requirement before saving."""
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        return password
    

    def to_dict(self):
        """Return a dictionary representation of the user including sensitive data."""
        return {
            '_id': self.id,
            '_first_name': self.first_name,
            '_last_name': self.last_name,
            '_email': self.email,
            '_password': self.password
        }

    def to_safe_dict(self):
        """Return a dictionary without the password field"""
        return {
            '_id': self.id,
            '_first_name': self.first_name,
            '_last_name': self.last_name,
            '_email': self.email,
            '_is_admin': self.is_admin
        }

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')


    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
