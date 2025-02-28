from app.models.base_model import BaseModel

class Amenity(BaseModel):
    """Represent an amenity to a place"""
    def __init__(self, id, name, **kwargs):
        super().__init__(**kwargs)
        self.id = id
        self.name = name

    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)
