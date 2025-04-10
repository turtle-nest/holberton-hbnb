#!/usr/bin/python3

import unittest
from app import create_app

class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
