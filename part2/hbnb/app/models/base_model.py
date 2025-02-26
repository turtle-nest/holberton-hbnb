import uuid
from datetime import datetime

class BaseModel:
	"""Base Model for all amenties"""
	def __init__(self, id=None, created_at=None, updated_at=None):
		self.id = id if id else str(uuid.uuid4())
		self.created_at = created_at if created_at else datetime.utcnow()
		self.updated_at = updated_at if updated_at else datetime.utcnow()

	def save(self):
		self.updated_at = datetime.utcnow()
