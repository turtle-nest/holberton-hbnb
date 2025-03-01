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
        self.name = name
        self.description = description
        self.city = city
        self.owner_id = owner_id
        self.latitude = latitude
        self.longitude = longitude
        self.price = price
        self.reviews = []
        self.amenities = []

        if amenities:
            for amenity_id in amenities:
                amenity = self.get_amenity_by_id(amenity_id)
                if amenity:
                    self.amenities.append(amenity)

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
        if value is None:
            raise ValueError("Name cannot be None")
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
    def city(self):
        """Get the place's city."""
        return self._city

    @city.setter
    def city(self, value):
        """Set the place's city."""
        if not isinstance(value, str):
            raise TypeError("City must be a string")
        if not value.strip():
            raise ValueError("City cannot be empty")
        self._city = value

    @property
    def owner_id(self):
        """Get the place's owner ID."""
        return self._owner_id

    @owner_id.setter
    def owner_id(self, value):
        """Set the place's owner ID."""
        if value is None:
            raise ValueError("Owner ID cannot be None")
        if not isinstance(value, str):
            raise TypeError("Owner ID must be a string")
        if not value.strip():
            raise ValueError("Owner ID cannot be empty")
        self._owner_id = value

    @property
    def price(self):
        """Get the place's price."""
        return self._price

    @price.setter
    def price(self, value):
        """Set the place's price."""
        if value is None:
            raise ValueError("Price cannot be None")
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a number")
        if value <= 0:
            raise ValueError("Price must be a positive number")
        self._price = value

    @property
    def latitude(self):
        """Get the place's latitude."""
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        """Set the place's latitude."""
        if value is None:
            raise ValueError("Latitude cannot be None")
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
        if value is None:
            raise ValueError("Longitude cannot be None")
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

    def validate_price(self):
        """Validate the price attribute."""
        if not isinstance(self._price, (int, float)) or self._price <= 0:
            raise ValueError("Price must be a positive number")

    def validate_latitude(self):
        """Validate the latitude attribute."""
        if not isinstance(self._latitude, (int, float)) or not (-90 <= self._latitude <= 90):
            raise ValueError("Latitude must be a float between -90 and 90")

    def validate_longitude(self):
        """Validate the longitude attribute."""
        if not isinstance(self._longitude, (int, float)) or not (-180 <= self._longitude <= 180):
            raise ValueError("Longitude must be a float between -180 and 180")
