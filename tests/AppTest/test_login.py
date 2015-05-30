import unittest
from flask import current_app
from backend import create_app, db
from backend.user.models import Role, User
from backend.blog.models import Post


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
        return self.client.post('/u/login', data=dict(
            email=e,
            password=p
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/u/logout', follow_redirects=True)

    def test_empty_db(self):
        p = Post.query.all()
        assert len(p) is 0

    def test_can_login(self):
        rv = self.login('test@mail.com', 'testpass')
        assert 'Test User' in rv.data
        rv = self.logout()
        assert 'logged out' in rv.data
        rv = self.login('tets@gmail.com', 'po')
        assert 'Invalid combination' in rv.data

    def test_add_post(self):
        self.login('test@mail.com', 'testpass')
        rv = self.client.post('/blog/new', data=dict(
            title='Title',
            description='Desc',
            body='## hello'
            ), follow_redirects=True)
        assert '<h2>hello</h2>' in rv.data

        rv = self.client.get('/blog/12')
        assert rv.status_code == 404
