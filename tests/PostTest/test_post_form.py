import unittest

from flask import url_for

from yapper import create_app, db
from yapper.blueprints.user.models import Role, User


class UserFormTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.client = self.app.test_client()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        u = User(
            email=self.app.config['FLASKY_ADMIN'],
            password='testpass',
            name='Admin'
        )
        u2 = User(
            email='test2@example.com',
            password='testpass',
            name='Test User 2',
            status=True
        )
        u3 = User(
            email='test3@example.com',
            password='testpass',
            name='Test User 3',
            status=True
        )
        db.session.add_all([u, u2, u3])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self, username, password):
        return self.client.post(url_for('user.login'), data=dict(
            email=username,
            password=password,
            remember_me='y'
        ), follow_redirects=True)

    def logout(self):
        return self.client.get(url_for('user.logout'), follow_redirects=False)

    def test_post_with_empty_field(self):
        rv = self.login(self.app.config['FLASKY_ADMIN'], 'testpass')
        rv = self.client.post(url_for('blog.add'), data=dict(
            title='Hello'
        ), follow_redirects=False)
        assert 'Provide a description' in rv.data

    def test_post_create_via_form(self):
        rv = self.login('test2@example.com', 'testpass')
        rv = self.client.post(url_for('blog.add'), data=dict(
            title='Hello',
            description='Hi',
            body='# Hello World'
        ), follow_redirects=True)
        assert '<h1>Hello World</h1>' in rv.data

    def test_post_deletable_by_author(self):
        rv = self.login('test2@example.com', 'testpass')
        rv = self.client.post(url_for('blog.add'), data=dict(
            title='Hello',
            description='Hi',
            body='### Hello World'
        ), follow_redirects=True)
        assert '<h3>Hello World</h3>' in rv.data
        rv = self.client.delete(
            url_for('blog.delete', pid=1), follow_redirects=True)
        assert rv.status_code == 200
        assert 'Post deleted.' in rv.data

    def test_post_by_u1_not_deletable_by_u2(self):
        rv = self.login('test2@example.com', 'testpass')
        rv = self.client.post(url_for('blog.add'), data=dict(
            title='Hello',
            description='Hi',
            body='### Hello World'
        ), follow_redirects=True)
        assert '<h3>Hello World</h3>' in rv.data
        rv = self.logout()
        assert rv.status_code == 302
        rv = self.client.delete(
            url_for('blog.delete', pid=1), follow_redirects=True)
        assert rv.status_code == 403

    def test_any_post_deletable_by_admin(self):
        rv = self.login('test2@example.com', 'testpass')
        rv = self.client.post(url_for('blog.add'), data=dict(
            title='Hello',
            description='Hi',
            body='### Hello World'
            ), follow_redirects=True)
        assert rv.status_code == 200
        assert 'Test User 2' in rv.data
        rv = self.logout()
        assert rv.status_code == 302
        rv = self.login(self.app.config['FLASKY_ADMIN'], 'testpass')
        rv = self.client.delete(
            url_for('blog.delete', pid=1), follow_redirects=True)
        assert rv.status_code == 200
        assert 'class="message success"><p>Post deleted.</p>' in rv.data
        rv = self.client.get(
            url_for('blog.get_post', pid=1))
        self.assertTrue(rv.status_code == 404)
        rv = self.client.post(url_for('blog.add'), data=dict(
            title='Hello',
            description='Hi',
            body='### Hello World'
            ), follow_redirects=True)
        self.assertTrue('<h3>Hello World</h3>' in rv.data)
