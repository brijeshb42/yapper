import unittest

from yapper import db
from yapper.blueprints.user.models import User, Role, Permission, AnonymousUser
from config import Config


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        db.create_all()
        Role.insert_roles()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_setter(self):
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_roles_and_permissions(self):
        u = User(email='user@gmail.com', password='adt')
        self.assertTrue(u.can(Permission.WRITE_POSTS))

    def test_admin(self):
        Role.insert_roles()
        u = User(email=Config.FLASKY_ADMIN, password='adt')
        self.assertTrue(u.is_admin())

    def test_anon_user(self):
        u = AnonymousUser()
        self.assertTrue(u.id == -1)
        self.assertFalse(u.can(Permission.WRITE_POSTS))
