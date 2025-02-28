#!/usr/bin/python3

import unittest
import json
from app import app
from app.models.place import Place

class TestReviewModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Setup class with Flask app before tests."""
        cls.client = app.test_client()

    def setUp(self):
        """Setup before each test."""
        self.place = Place(name="Test Place", description="A place for testing")
        self.place.save()  # Save to the database (adjust depending on your ORM)
        self.valid_review_data = {
            "text": "This is a great place!",
            "place_id": self.place.id
        }
        self.invalid_review_data = {
            "text": "This is an invalid review without a place_id"
        }

    def tearDown(self):
        """Cleanup after each test."""
        self.place.delete()  # Remove the place after test (adjust depending on your ORM)

    def test_create_review_success(self):
        """Test creating a review."""
        response = self.client.post('/api/v1/reviews/', data=json.dumps(self.valid_review_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)  # Check if the review is created
        response_json = json.loads(response.data)
        self.assertIn('id', response_json)  # Ensure the response contains the ID of the created review

    def test_create_review_invalid(self):
        """Test creating a review with invalid data."""
        response = self.client.post('/api/v1/reviews/', data=json.dumps(self.invalid_review_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)  # Check for Bad Request (400)
        response_json = json.loads(response.data)
        self.assertIn('error', response_json)  # Ensure the response contains an error message

    def test_get_reviews(self):
        """Test retrieving all reviews."""
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data)
        self.assertIsInstance(response_json, list)  # Ensure the response is a list of reviews

    def test_get_reviews_for_place(self):
        """Test retrieving reviews for a specific place."""
        # First, create a review for the place
        self.client.post('/api/v1/reviews/', data=json.dumps(self.valid_review_data), content_type='application/json')
        response = self.client.get(f'/api/v1/places/{self.place.id}/reviews')
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data)
        self.assertIsInstance(response_json, list)  # Ensure the response is a list of reviews for the place

    def test_update_review_success(self):
        """Test updating a review."""
        # First, create a review
        create_response = self.client.post('/api/v1/reviews/', data=json.dumps(self.valid_review_data),
                                           content_type='application/json')
        review_id = json.loads(create_response.data)['id']

        # Now, update the review
        updated_data = {"text": "Updated review text!"}
        response = self.client.put(f'/api/v1/reviews/{review_id}', data=json.dumps(updated_data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)  # Ensure the review is updated
        response_json = json.loads(response.data)
        self.assertEqual(response_json['text'], updated_data['text'])  # Ensure the review text is updated

    def test_delete_review_success(self):
        """Test deleting a review."""
        # First, create a review
        create_response = self.client.post('/api/v1/reviews/', data=json.dumps(self.valid_review_data),
                                           content_type='application/json')
        review_id = json.loads(create_response.data)['id']

        # Now, delete the review
        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)  # Ensure the review is deleted

        # Check that the review no longer exists
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 404)  # The review should be gone

    @classmethod
    def tearDownClass(cls):
        """Cleanup after all tests."""
        pass


if __name__ == '__main__':
    unittest.main()
