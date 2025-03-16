from app import db
from app.persistence.repository import SQLAlchemyRepository

# Review Repository
from app.models.review import Review

class ReviewRepository(SQLAlchemyRepository):
    """
    Repository for interacting with the Review model.
    """
    def __init__(self):
        super().__init__(Review)
