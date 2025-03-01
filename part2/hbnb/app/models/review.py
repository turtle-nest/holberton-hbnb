from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place

"""Module that defines the Review class"""

class Review(BaseModel):
    """Review class with specific attributes and relationships"""
    def __init__(self, text, rating, user_id, place_id, **kwargs):
        """Initialize a new Review instance"""
        super().__init__(**kwargs)
        if not text:
            raise ValueError("Review text cannot be empty")
        self.text = text
        self.rating = self.validate_rating(rating)
        self.user_id = self.validate_user(user_id)
        self.place_id = self.validate_place(place_id)

    def validate_rating(self, rating):
        """Ensure the rating is an integer between 1 and 5"""
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        return rating

    def validate_place(self, place_id):
        """Ensure the place_id is valid and exists"""
        place = Place.get(place_id)
        if not place:
            raise ValueError("Invalid place_id: Place not found")
        return place_id

    def validate_user(self, user_id):
        """Ensure the user_id is valid and exists"""
        user = User.get(user_id)
        if not user:
            raise ValueError("Invalid user_id: User not found")
        return user_id
