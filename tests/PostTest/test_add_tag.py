import unittest
from yapper import db, create_app
from yapper.blueprints.blog.models import Post, Tag, Category
from yapper.blueprints.user.models import User


class TagAddTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_tag_creation(self):
        tag = Tag(name='node.js')
        self.assertTrue(tag.id is None)
        db.session.add(tag)
        db.session.commit()
        self.assertTrue(tag.id >= 1)

    def test_category_creation(self):
        cat = Category(name='node.js')
        self.assertTrue(cat.id is None)
        db.session.add(cat)
        db.session.commit()
        self.assertTrue(cat.id >= 1)

    def test_post_creation(self):
        u = User(
            email=self.app.config['FLASKY_ADMIN'],
            password='testpass',
            name='Admin'
        )
        tag = Tag(name='node.js')
        cat = Category(name='node.js')
        db.session.add(u)
        db.session.add(tag)
        db.session.add(cat)
        db.session.commit()
        post = Post(
            author=u,
            title='Test Post',
            content='# Hello',
            tags=[tag],
            categories=[cat]
        )
        self.assertTrue(post.id is None)
        db.session.add(post)
        db.session.commit()
        self.assertTrue(post.id > 0)
        self.assertTrue(tag.posts.first().id == post.id)
        self.assertTrue(cat.posts.first().id == post.id)
        self.assertTrue(post.tags[0].id == tag.id)
        self.assertTrue(post.categories[0].id == cat.id)
