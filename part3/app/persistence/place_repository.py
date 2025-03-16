from app import db
from app.persistence.repository import SQLAlchemyRepository

# Place Repository
from app.models.place import Place

class PlaceRepository(SQLAlchemyRepository):
    """
    Repository for interacting with the Place model.
    """
    def __init__(self):
        super().__init__(Place)
