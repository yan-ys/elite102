import unittest
from main import withdraw

from main import create_account

class Tests(unittest.TestCase):

    def test_withdraw(self):
        self.assertEqual(withdraw(-1, 200), "Account not found.")
    def test_create_account(self):
        self.assertIsNotNone(create_account("Alice", 200.0))

if __name__ == '__main__':
    unittest.main()