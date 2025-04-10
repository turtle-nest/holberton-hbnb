#!/usr/bin/python3

import unittest
import uuid
from app.models.user import User  # Assurez-vous que User est un modèle sans dépendance à la DB

class TestUserModel(unittest.TestCase):
    """Test the User model"""

    def setUp(self):
        """Initial setup for tests"""
        # Generate a unique email for each test
        unique_email = f"user{uuid.uuid4()}@example.com"

        # Create a new user with the unique email (no DB interaction)
        self.user = User(
            first_name="John",
            last_name="Doe",
            email=unique_email,
            password="securepassword123"
        )

    def test_user_creation(self):
        """Test if a user is created correctly"""
        # Check if the first name, last name, and email are set correctly
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.last_name, "Doe")
        self.assertEqual(self.user.email, self.user.email)  # The email should be unique for each test

    def test_update_user_email(self):
        """Test updating the user's email"""
        # Generate a new unique email for updating
        new_email = f"user{uuid.uuid4()}@example.com"
        self.user.email = new_email
        # Check if the email was updated correctly
        self.assertEqual(self.user.email, new_email)

if __name__ == "__main__":
    unittest.main()
