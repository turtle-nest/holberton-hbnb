from app import db
import uuid
from datetime import datetime, timezone

class BaseModel(db.Model):
    """Abstract base model that provides common attributes and methods for other models."""
    __abstract__ = True  # This ensures SQLAlchemy does not create a table for BaseModel

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))


    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()
        db.session.add(self)
        db.session.commit()


    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp


    def is_max_length(self, name, value, max_length):
        """Validate that a string does not exceed the maximum length."""
        if len(value) > max_length:
            raise ValueError(f"{name} must be {max_length} characters max.") 


    def is_between(self, name, value, min, max):
        """Validate that a numerical value is within a specified range."""
        if not min < value < max:
            raise ValueError(f"{name} must be between {min} and {max}.")
