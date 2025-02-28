import unittest
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository

class TestAmenityModel(unittest.TestCase):
    def setUp(self):
        self.repo = InMemoryRepository()
        self.amenity_data = {
            "id": "123",
            "name": "Pool"
        }
        self.amenity = Amenity(**self.amenity_data)
        self.repo.add(self.amenity)

    def test_create_amenity(self):
        new_amenity_data = {"id": "456", "name": "WiFi"}
        new_amenity = Amenity(**new_amenity_data)
        self.repo.add(new_amenity)
        self.assertEqual(self.repo.get("456"), new_amenity)

    def test_get_all_amenities(self):
        amenities = self.repo.get_all()
        self.assertIn(self.amenity, amenities)

    def test_get_amenity(self):
        amenity = self.repo.get("123")
        self.assertEqual(amenity, self.amenity)

    def test_get_non_existent_amenity(self):
        amenity = self.repo.get("999")
        self.assertIsNone(amenity)

    def test_update_amenity(self):
        updated_data = {"name": "Updated Pool"}
        self.amenity.update(updated_data)
        self.repo.update(self.amenity)
        updated_amenity = self.repo.get("123")
        self.assertEqual(updated_amenity.name, "Updated Pool")

    def test_update_non_existent_amenity(self):
        non_existent = Amenity(id="999", name="Non-existent")
        result = self.repo.update(non_existent.id, updated_data)
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
