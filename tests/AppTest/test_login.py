import unittest

from flask import url_for

from yapper import create_app, db
from yapper.blueprints.user.models import Role, User
from yapper.blueprints.blog.models import Post


class LoginTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app.config['CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        role = Role.query.filter_by(name='user').first()
        user = User(
            name='Test User',
            email='test@mail.com',
            password='testpass',
            status=True,
            role=role
        )
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self, e, p):
        return self.client.post(url_for('user.login'), data=dict(
            email=e,
            password=p
        ), follow_redirects=True)

    def logout(self):
        return self.client.get(url_for('user.logout'), follow_redirects=True)

    def test_empty_db(self):
        p = Post.query.all()
        assert len(p) is 0

    def test_can_login(self):
        rv = self.login('test@mail.com', 'testpass')
        assert 'Test User' in rv.data
        rv = self.logout()
        assert 'You have been logged out' in rv.data
        rv = self.login('test@gmail.com', 'po')
        assert 'Invalid combination' in rv.data

    def test_add_post(self):
        self.login('test@mail.com', 'testpass')
        rv = self.client.post(url_for('blog.add'), data=dict(
            title='Title',
            description='Desc',
            body='## hello there'
            ), follow_redirects=True)
        assert '<h2>hello there</h2>' in rv.data

        rv = self.client.get(
            url_for(
                'blog.get_post_by_slug',
                slug='some-slug-that-is-not-there'))
        assert rv.status_code == 404
