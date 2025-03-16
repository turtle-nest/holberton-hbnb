from app.models.basemodel import BaseModel
from app.models.review import Review
from app.models.amenity import Amenity
from sqlalchemy.orm import validates
from app import db

class Place(BaseModel):
    """Place model representing a rental location."""
    __tablename__ = 'places'

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    owner = db.relationship('User', backref='places', lazy=True)
    reviews = db.relationship('Review', backref='place_reviews', lazy=True)
    amenities = db.relationship('Amenity', secondary='place_amenity', backref='place')


    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)
    
    def delete_review(self, review):
        """Add an amenity to the place."""
        self.reviews.remove(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)


    @validates('title')
    def validate_title(self, key, value):
        """Ensure title is a non-empty string."""
        if not isinstance(value, str):
            raise TypeError(f"{key} must be a string")
        if not value.strip():
            raise ValueError(f"{key} cannot be empty")
        if len(value) > 100:
            raise ValueError(f"{key} must be 100 characters max")
        return value.strip()

    @validates('price')
    def validate_price(self, key, value):
        """Ensure price is a positive number."""
        try:
            value = float(value)
        except ValueError:
            raise TypeError(f"{key} must be a float or integer")

        if value < 0:
            raise ValueError(f"{key} must be positive")
        return value

    @validates('latitude')
    def validate_latitude(self, key, value):
        """Ensure latitude is between -90 and 90."""
        try:
            value = float(value)
        except ValueError:
            raise TypeError(f"{key} must be a float")

        if not (-90 <= value <= 90):
            raise ValueError(f"{key} must be between -90 and 90")
        return value
    
    @validates('longitude')
    def validate_longitude(self, key, value):
        """Ensure longitude is between -180 and 180."""
        try:
            value = float(value)
        except ValueError:
            raise TypeError(f"{key} must be a float")

        if not (-180 <= value <= 180):
            raise ValueError(f"{key} must be between -180 and 180")
        return value

    def to_dict(self):
        """Return a dictionary representation of the place."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude
        }

    def to_safe_dict(self):
        """Return a dictionary without sensitive data (if any)."""
        return self.to_dict()

    def to_dict_list(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
        }
