import uuid
from datetime import datetime
"""Module to define a BaseModel class"""

class BaseModel:
    """Base model with common attributes and methods"""
    def __init__(self):
        """
        Initialize a new BaseModel instance with unique ID and timestamps
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """
        Update the updated_at timestamp whenever the object is modified
        """
        self.updated_at = datetime.now()

    def to_dict(self):
        """Converts object to dictionary"""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
