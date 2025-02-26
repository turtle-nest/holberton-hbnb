from app.models.base_model import BaseModel

class Review(BaseModel):
	"""Represent a review in a place"""
	def __init__(self, place_id, user_id, text, **kwargs):
		super().__init__(**kwargs)
		self.place_id = place_id
		self.user_id = user_id
		self.text = text
