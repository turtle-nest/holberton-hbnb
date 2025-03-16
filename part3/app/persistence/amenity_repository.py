from app import db
from app.persistence.repository import SQLAlchemyRepository

# Amenity Repository
from app.models.amenity import Amenity

class AmenityRepository(SQLAlchemyRepository):
    """
    Repository for interacting with the Amenity model.
    """
    def __init__(self):
        super().__init__(Amenity)
