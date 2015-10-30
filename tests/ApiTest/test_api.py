import unittest
import json

from flask import url_for

from yapper import create_app, db
from yapper.blueprints.blog.models import Tag, Category


TEST_ACCESS_TOKEN = 'hello'


class ModelAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.client = self.app.test_client()
        self.app_context.push()
        db.create_all()
        tag = Tag(name="tag")
        tag.save()
        category = Category(name="category")
        category.save()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_tag_without_token(self):
        rv = self.client.get(url_for('api.tag_api'), follow_redirects=False)
        assert rv.status_code == 403

    def test_category_without_token(self):
        rv = self.client.get(
            url_for('api.category_api'), follow_redirects=False)
        assert rv.status_code == 403

    def test_tag_with_token(self):
        rv = self.client.get(
            url_for('api.tag_api'),
            headers={'Access-Token': TEST_ACCESS_TOKEN},
            follow_redirects=False)
        data = json.loads(rv.data)
        assert 'type' in data
        assert 'data' in data
        assert data['type'] == 'success'
        assert len(data['data']) == 1
        assert data['data'][0]['name'] == 'tag'
        assert rv.status_code == 200

    def test_category_with_token(self):
        rv = self.client.get(
            url_for('api.category_api'),
            headers={'Access-Token': TEST_ACCESS_TOKEN},
            follow_redirects=False)
        data = json.loads(rv.data)
        assert 'type' in data
        assert 'data' in data
        assert data['type'] == 'success'
        assert len(data['data']) == 1
        assert data['data'][0]['name'] == 'category'
        assert rv.status_code == 200
