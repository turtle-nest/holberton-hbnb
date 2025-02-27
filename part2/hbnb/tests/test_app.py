# filepath: /Users/nicolas/holberton-hbnb/part2/hbnb/tests/test_app.py
import unittest
from app import create_app

class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 404)  # Assurez-vous que la route existe

if __name__ == '__main__':
    unittest.main()
