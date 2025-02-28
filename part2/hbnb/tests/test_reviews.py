import unittest
from unittest.mock import patch, MagicMock
from app import create_app
from app.services import facade

class TestReviewsAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

    @patch('app.services.facade.create_review')
    def test_create_review_success(self, mock_create_review):
        mock_review = MagicMock(
            id='1', text='Great place!', rating=5, user_id='user1', place_id='place1',
            created_at='2025-02-28T12:00:00', updated_at='2025-02-28T12:00:00'
        )
        mock_create_review.return_value = mock_review

        response = self.client.post('/reviews/', json={
            'text': 'Great place!',
            'rating': 5,
            'user_id': 'user1',
            'place_id': 'place1'
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['text'], 'Great place!')

    @patch('app.services.facade.get_all_reviews')
    def test_get_all_reviews(self, mock_get_all_reviews):
        mock_review = MagicMock(
            id='1', text='Great place!', rating=5, user_id='user1', place_id='place1',
            created_at='2025-02-28T12:00:00', updated_at='2025-02-28T12:00:00'
        )
        mock_get_all_reviews.return_value = [mock_review]

        response = self.client.get('/reviews/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    @patch('app.services.facade.get_review_by_id')
    def test_get_review_by_id_not_found(self, mock_get_review_by_id):
        mock_get_review_by_id.return_value = None

        response = self.client.get('/reviews/1')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], 'Review not found')

    @patch('app.services.facade.update_review')
    def test_update_review_success(self, mock_update_review):
        mock_review = MagicMock(
            id='1', text='Updated review!', rating=4, user_id='user1', place_id='place1',
            created_at='2025-02-28T12:00:00', updated_at='2025-02-28T12:05:00'
        )
        mock_update_review.return_value = mock_review

        response = self.client.put('/reviews/1', json={
            'text': 'Updated review!',
            'rating': 4,
            'user_id': 'user1',
            'place_id': 'place1'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['text'], 'Updated review!')

    @patch('app.services.facade.delete_review')
    def test_delete_review_success(self, mock_delete_review):
        mock_delete_review.return_value = True

        response = self.client.delete('/reviews/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Review deleted successfully')

if __name__ == '__main__':
    unittest.main()
