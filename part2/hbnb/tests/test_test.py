#!/usr/bin/python3
import unittest

class TestSimple(unittest.TestCase):
    def test_addition(self):
        """Test simple addition"""
        self.assertEqual(2 + 3, 4)

if __name__ == "__main__":
    unittest.main()
