#!/usr/bin/python3

import unittest
from app import create_app

class TestPlaceModel(unittest.TestCase):
    """Test the Place model"""

    @classmethod
    def setUpClass(cls):
        """Set up the application and test client"""
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def setUp(self):
        """Initial setup for each test"""
        self.place_data = {
            "name": "Test Place",
            "location": "Test Location",
            "description": "A place for testing."
        }

    def test_create_place_success(self):
        """Test if a place is created successfully"""
        response = self.client.post('/places', json=self.place_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)  # Ensure the response includes the created place ID
        self.assertIsNotNone(response.json['id'], "ID should not be None")

    def test_get_place_success(self):
        """Test if a place can be retrieved successfully"""
        # First, create a place
        create_response = self.client.post('/places', json=self.place_data)
        self.assertEqual(create_response.status_code, 201)
        
        place_id = create_response.json['id']
        self.assertIsNotNone(place_id, "Place ID should not be None")

        # Now retrieve the place
        response = self.client.get(f'/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], self.place_data['name'])

    def test_update_place_success(self):
        """Test if a place is updated successfully"""
        # First, create a place
        create_response = self.client.post('/places', json=self.place_data)
        self.assertEqual(create_response.status_code, 201)
        
        place_id = create_response.json['id']
        self.assertIsNotNone(place_id, "Place ID should not be None")

        # Now update the place
        update_data = {"name": "Updated Place", "location": "New Location", "description": "Updated description."}
        response = self.client.put(f'/places/{place_id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], update_data['name'])

    def test_create_place_invalid_data(self):
        """Test if an invalid place creation returns a 400 Bad Request"""
        invalid_data = {
            "name": "",  # Invalid name
            "location": "Invalid Location"
        }
        response = self.client.post('/places', json=invalid_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)  # Ensure the response contains the error message

if __name__ == "__main__":
    unittest.main()
