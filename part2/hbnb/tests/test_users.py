#!/usr/bin/python3

import unittest
from app.models.user import User

class TestUserModel(unittest.TestCase):
    """Test the User model"""

    def setUp(self):
        """Initial setup for tests"""
        self.user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="securepassword123"
        )

    def test_user_creation(self):
        """Test if a user is created correctly"""
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.last_name, "Doe")
        self.assertEqual(self.user.email, "john.doe@example.com")

    def test_update_user_email(self):
        """Test updating user's email"""
        self.user.email = "new.email@example.com"
        self.assertEqual(self.user.email, "new.email@example.com")

if __name__ == "__main__":
    unittest.main()
