"""
(c) 2014 by Brijesh Bittu
"""
import unittest
from app.user.forms import LoginForm


class UserFormTestCase(unittest.TestCase):
    def test_valid_email(self):
        form = LoginForm()
        form.email = 'b2@gmail.com'
        form.password = '1234'
        self.assertTrue(True)
