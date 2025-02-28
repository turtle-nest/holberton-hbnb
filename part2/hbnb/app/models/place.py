from app.models.base_model import BaseModel
from app.models.place_review import PlaceReview
from app.models.user import User
from app.models.amenity import Amenity

"""Module that defines the Place class."""

class Place(BaseModel):
    """Place class that inherits from BaseModel.
    Represents a rental place with its attributes and relationships.
    """
    def __init__(self, name, description, city, owner_id, latitude, longitude, price, amenities=None):
        """Initialize a new Place instance."""
        super().__init__()
        self._name = name
        self._description = description
        self._city = city
        self._owner_id = owner_id
        self._latitude = latitude
        self._longitude = longitude
        self._price = price
        self._reviews = []
        self._amenities = []

        if amenities:
            for amenity_id in amenities:
                amenity = self.get_amenity_by_id(amenity_id)
                if amenity:
                    self._amenities.append(amenity)

        # Validate attributes
        self.validate_price()
        self.validate_latitude()
        self.validate_longitude()

    @property
    def name(self):
        """Get the place's name."""
        return self._name

    @name.setter
    def name(self, value):
        """Set the place's name."""
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value

    @property
    def description(self):
        """Get the place's description."""
        return self._description

    @description.setter
    def description(self, value):
        """Set the place's description."""
        if not isinstance(value, str):
            raise TypeError("Description must be a string")
        self._description = value

    @property
    def price(self):
        """Get the place's price."""
        return self._price

    @price.setter
    def price(self, value):
        """Set the place's price."""
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Price must be a non-negative float")
        self._price = value

    @property
    def latitude(self):
        """Get the place's latitude."""
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        """Set the place's latitude."""
        if not isinstance(value, (int, float)) or not (-90 <= value <= 90):
            raise ValueError("Latitude must be a float between -90 and 90")
        self._latitude = value

    @property
    def longitude(self):
        """Get the place's longitude."""
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        """Set the place's longitude."""
        if not isinstance(value, (int, float)) or not (-180 <= value <= 180):
            raise ValueError("Longitude must be a float between -180 and 180")
        self._longitude = value

    @property
    def reviews(self):
        """Get the list of reviews."""
        return self._reviews

    def add_review(self, review_text, rating, user_id):
        """Add a review to the place."""
        review = PlaceReview(review_text, rating, user_id)
        self._reviews.append(review)

    @property
    def amenities(self):
        """Get the list of amenities."""
        return self._amenities

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        if not isinstance(amenity, Amenity):
            raise ValueError("Amenity must be an instance of the Amenity class")
        self._amenities.append(amenity)

    def set_owner(self, owner):
        """Set the owner of the place."""
        if not isinstance(owner, User):
            raise ValueError("Owner must be an instance of the User class")
        self._owner_id = owner.id

    def get_amenity_by_id(self, amenity_id):
        """Retrieve an Amenity object by its ID."""
        return Amenity(id=amenity_id, name=f"Amenity {amenity_id}")
