import unittest
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class TestModels(unittest.TestCase):
    """Class to test all the models and their methods"""

    def setUp(self):
        """Set up test data for each test"""
        self.user = User("John", "Doe", "john.doe@example.com", "password123")
        self.place = Place(
            name="Cozy Cottage", 
            description="A cozy cottage for a perfect vacation", 
            city="Paris", 
            owner_id="12345", 
            latitude=48.8566, 
            longitude=2.3522, 
            price=100
        )
        self.amenity = Amenity(id="1", name="Wi-Fi")
        self.review = Review(
            text="Amazing place with great amenities", 
            rating=5, 
            user_id="12345", 
            place_id="67890"
        )

    def test_user_creation_valid(self):
        """Test creating a valid user"""
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.last_name, "Doe")
        self.assertEqual(self.user.email, "john.doe@example.com")
        self.assertEqual(self.user.password, "password123")
        self.assertFalse(self.user.is_admin)

    def test_user_creation_invalid_email_format(self):
        """Test creating a user with an invalid email format"""
        with self.assertRaises(ValueError):
            self.user.email = "invalid-email-format"

    def test_user_creation_duplicate_email(self):
        """Test creating a user with an already existing email"""
        another_user = User("Jane", "Smith", "john.doe@example.com", "password123")
        with self.assertRaises(ValueError):
            another_user.email = "john.doe@example.com"

    def test_user_creation_empty_first_name(self):
        """Test creating a user with an empty first name"""
        with self.assertRaises(ValueError):
            self.user.first_name = ""

    def test_user_creation_empty_last_name(self):
        """Test creating a user with an empty last name"""
        with self.assertRaises(ValueError):
            self.user.last_name = ""

    def test_user_creation_invalid_password(self):
        """Test creating a user with a short password"""
        with self.assertRaises(ValueError):
            self.user.password = "short"

    def test_review_creation_valid(self):
        """Test creating a valid review"""
        self.assertEqual(self.review.text, "Amazing place with great amenities")
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.user_id, "12345")
        self.assertEqual(self.review.place_id, "67890")

    def test_review_creation_invalid_rating(self):
        """Test creating a review with an invalid rating"""
        with self.assertRaises(ValueError):
            self.review.rating = 6  # Rating outside valid range

    def test_review_creation_empty_text(self):
        """Test creating a review with empty text"""
        with self.assertRaises(ValueError):
            self.review.text = ""

    def test_place_creation_valid(self):
        """Test creating a valid place"""
        self.assertEqual(self.place.name, "Cozy Cottage")
        self.assertEqual(self.place.city, "Paris")
        self.assertEqual(self.place.price, 100)
        self.assertEqual(self.place.latitude, 48.8566)
        self.assertEqual(self.place.longitude, 2.3522)

    def test_place_creation_invalid_price(self):
        """Test creating a place with an invalid price"""
        with self.assertRaises(ValueError):
            self.place.price = -50  # Invalid price

    def test_place_creation_invalid_latitude(self):
        """Test creating a place with an invalid latitude"""
        with self.assertRaises(ValueError):
            self.place.latitude = 100  # Latitude out of bounds

    def test_place_creation_invalid_longitude(self):
        """Test creating a place with an invalid longitude"""
        with self.assertRaises(ValueError):
            self.place.longitude = 200  # Longitude out of bounds

    def test_place_add_review(self):
        """Test adding a review to a place"""
        self.place.add_review("Great place", 4, "12345")
        self.assertEqual(len(self.place.reviews), 1)

    def test_place_add_amenity(self):
        """Test adding an amenity to a place"""
        self.place.add_amenity(self.amenity)
        self.assertIn(self.amenity, self.place.amenities)

    def test_place_add_invalid_amenity(self):
        """Test adding an invalid amenity to a place"""
        with self.assertRaises(ValueError):
            self.place.add_amenity("Invalid Amenity")

    def test_place_set_owner(self):
        """Test setting the owner of a place"""
        self.place.set_owner(self.user)
        self.assertEqual(self.place.owner_id, self.user.id)

    def test_place_set_invalid_owner(self):
        """Test setting an invalid owner for a place"""
        with self.assertRaises(ValueError):
            self.place.set_owner("NotAUser")

    def test_amenity_creation_valid(self):
        """Test creating a valid amenity"""
        self.assertEqual(self.amenity.id, "1")
        self.assertEqual(self.amenity.name, "Wi-Fi")

    def test_amenity_update(self):
        """Test updating an amenity"""
        self.amenity.update({"name": "Updated Wi-Fi"})
        self.assertEqual(self.amenity.name, "Updated Wi-Fi")

if __name__ == "__main__":
    unittest.main()
