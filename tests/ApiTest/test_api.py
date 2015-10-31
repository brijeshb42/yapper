import unittest
import json

from flask import url_for, Response

from yapper import create_app, db
from yapper.lib.response import json_error, json_success
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
        category = Category(name="category")
        db.session.add(tag)
        db.session.add(category)
        db.session.commit()

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

    def test_tag_creation_by_empty_name(self):
        rv = self.client.post(
            url_for('api.tag_api'),
            headers={
                'Access-Token': TEST_ACCESS_TOKEN,
                'Content-Type': 'application/json'
            },
            data=json.dumps(dict(name='')),
            follow_redirects=False)
        data = json.loads(rv.data)
        assert 'type' in data
        assert 'data' in data
        assert data['type'] == 'error'
        assert 'name' in data['data']
        assert data['data']['name'][0] == 'Empty name'
        assert rv.status_code == 406

    def test_already_existing_tag_creation(self):
        rv = self.client.post(
            url_for('api.tag_api'),
            headers={
                'Access-Token': TEST_ACCESS_TOKEN,
                'Content-Type': 'application/json'
            },
            data=json.dumps(dict(name='tag')),
            follow_redirects=False)
        data = json.loads(rv.data)
        assert 'type' in data
        assert 'data' in data
        assert data['type'] == 'error'
        # assert 'name' in data['data']
        assert data['data'] == 'This item already exists.'
        assert rv.status_code == 406

    def test_new_tag_creation(self):
        rv = self.client.post(
            url_for('api.tag_api'),
            headers={
                'Access-Token': TEST_ACCESS_TOKEN,
                'Content-Type': 'application/json'
            },
            data=json.dumps(dict(name='new_tag')),
            follow_redirects=False)
        data = json.loads(rv.data)
        assert 'type' in data
        assert 'data' in data
        assert data['type'] == 'success'
        assert type(data['data']) == dict
        new_tag = data['data']
        assert 'id' in new_tag
        assert 'name' in new_tag
        assert 'created_at' in new_tag
        assert new_tag['name'] == 'new_tag'
        assert rv.status_code == 200

        rv = self.client.get(
            url_for('api.tag_api', m_id=new_tag['id']),
            headers={
                'Access-Token': TEST_ACCESS_TOKEN
            },
            follow_redirects=False
        )
        data = json.loads(rv.data)
        assert rv.status_code == 200
        assert data['type'] == 'success'
        assert data['data']['id'] == new_tag['id']
        assert data['data']['name'] == new_tag['name']

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

    def test_json_success(self):
        data = json_success(data='Hello success')
        rsp = json.loads(data.data)
        assert isinstance(data, Response)
        assert 'type' in rsp
        assert rsp['type'] == 'success'
        assert rsp['data'] == 'Hello success'

    def test_json_error(self):
        data = json_error(data='Hello error')
        assert len(data) == 2
        assert isinstance(data[0], Response)
        assert data[1] == 400
        rsp = json.loads(data[0].data)
        assert 'type' in rsp
        assert rsp['type'] == 'error'
        assert rsp['data'] == 'Hello error'
        data = json_error(data='Server error', code=500)
        assert len(data) == 2
        assert isinstance(data[0], Response)
        assert data[1] == 500
        rsp = json.loads(data[0].data)
        assert 'type' in rsp
        assert rsp['type'] == 'error'
        assert rsp['data'] == 'Server error'
