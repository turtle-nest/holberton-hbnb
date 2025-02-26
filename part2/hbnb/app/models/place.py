from app.models.base_model import BaseModel

class Place(BaseModel):
	"""Represent a place"""
	def __init__(self, name, description, owner_id, **kwargs):
		super().__init__(**kwargs)
		self.name = name
		self.description = description
		self.owner_id = owner_id
		self.amenities = []
