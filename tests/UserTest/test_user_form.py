"""
(c) 2014 by Brijesh Bittu
"""
import unittest
from flask import current_app
from app import create_app, db
from app.user.models import Role, User
from app.blog.models import Post


class UserFormTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app.config['CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        db.create_all()
        self.app_context.push()
        Role.insert_roles()
        u = User(
            email=self.app.config['FLASKY_ADMIN'],
            password='testpass',
            name='Admin',
        )
        u2 = User(
            email='test@example.com',
            password='testpass',
            name='Test',
            status=True
        )
        db.session.add(u)
        db.session.add(u2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self, username, password):
        return self.client.post('/u/login', data=dict(
            email=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/u/logout', follow_redirects=True)

    def test_post_with_empty_field(self):
        rv = self.login(self.app.config['FLASKY_ADMIN'], 'testpass')
        rv = self.client.post('/blog/add', data=dict(
            title='Hello'
        ), follow_redirects=False)
        assert 'Provide a description' in rv.data

    def test_post_add_via_form(self):
        rv = self.login('test@example.com', 'testpass')
        rv = self.client.post('/blog/add', data=dict(
            title='Hello',
            description='Hi',
            body='# Hello World'
        ), follow_redirects=True)
        assert '<h1>Hello World</h1>' in rv.data

    def test_admin_post_not_deleted_by_others(self):
        rv = self.login(self.app.config['FLASKY_ADMIN'], 'testpass')
        rv = self.client.post('/blog/add', data=dict(
            title='Hello',
            description='Hi',
            body='# Hello World'
        ), follow_redirects=True)
        assert '<h1>Hello World</h1>' in rv.data
        rv = self.logout()
        rv = self.login('test@example.com', 'testpass')
        rv = self.client.delete('/blog/1', follow_redirects=True)
        assert 'You cannot delete this post' in rv.data

