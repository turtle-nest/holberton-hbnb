from app.models.base_model import BaseModel

class Amenity(BaseModel):
	"""Represent an amenity to a place"""
    def __init__(self, name, **kwargs):
		super().__init__(**kwargs)
		self.name = name
