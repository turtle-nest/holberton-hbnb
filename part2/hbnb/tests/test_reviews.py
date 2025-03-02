import unittest
from app.models.review import Review
from app.models.user import User
from app.models.place import Place

class TestReview(unittest.TestCase):
    """Unit tests for the Review class"""

    def setUp(self):
        """Set up mock data for tests"""
        self.user = User(first_name="John", last_name="Doe", email="john.doe@example.com", password="password123")
        self.place = Place(name="Cozy Cabin", description="A nice cabin in the woods", city="Denver", owner_id=self.user.id, latitude=39.7392, longitude=-104.9903, price=100)
        User._existing_emails.add(self.user.email)

    def test_valid_review_creation(self):
        """Test successful creation of a valid review"""
        review = Review(text="Great place!", rating=5, user_id=self.user.id, place_id=self.place.id)
        self.assertEqual(review.text, "Great place!")
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.user_id, self.user.id)
        self.assertEqual(review.place_id, self.place.id)

    def test_empty_text_raises_value_error(self):
        """Test that an empty review text raises a ValueError"""
        with self.assertRaises(ValueError):
            Review(text="", rating=4, user_id=self.user.id, place_id=self.place.id)

    def test_invalid_rating_raises_value_error(self):
        """Test that an invalid rating raises a ValueError"""
        with self.assertRaises(ValueError):
            Review(text="Nice stay", rating=6, user_id=self.user.id, place_id=self.place.id)

    def test_nonexistent_user_raises_value_error(self):
        """Test that a non-existent user raises a ValueError"""
        with self.assertRaises(ValueError):
            Review(text="Nice stay", rating=4, user_id="invalid_user_id", place_id=self.place.id)

    def test_nonexistent_place_raises_value_error(self):
        """Test that a non-existent place raises a ValueError"""
        with self.assertRaises(ValueError):
            Review(text="Nice stay", rating=4, user_id=self.user.id, place_id="invalid_place_id")

if __name__ == "__main__":
    unittest.main()
