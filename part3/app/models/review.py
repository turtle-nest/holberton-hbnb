from app.models.basemodel import BaseModel
from sqlalchemy.orm import validates
from app import db
import uuid

class Review(BaseModel):
    """Review model representing user reviews for places."""
    __tablename__ = 'reviews'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    comment = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref='reviews')
    place = db.relationship('Place', backref='place_reviews')


    def __init__(self, text, rating):
        """Initialize a new review with required attributes."""
        super().__init__()
        self.text = text
        self.rating = rating

    @db.validates('rating')
    def validate_rating(self, key, rating):
        """Ensure rating is between 1 and 5."""
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        return rating


    def to_dict(self):
        """Return a dictionary representation of the review."""
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating
        }


    def to_safe_dict(self):
        """Return a dictionary without sensitive data (if any)."""
        return self.to_dict()
