import unittest
from backend import create_app, db
from backend.user.models import User, Role


class TestUserAddToDb(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_role_gets_id(self):
        role = Role(name='admin')
        self.assertTrue(role.id is None)
        db.session.add(role)
        db.session.commit()
        self.assertTrue(role.id is not None)

    def test_user_gets_id(self):
        role = Role(name='admin')
        db.session.add(role)
        db.session.commit()
        user = User(email='b2@gmail.com', password='1234', role=role)
        self.assertFalse(role.id is None)
        self.assertTrue(user.id is None)
        db.session.add(user)
        db.session.commit()
        self.assertFalse(user.id is None)
        self.assertTrue(user.role_id == role.id)
