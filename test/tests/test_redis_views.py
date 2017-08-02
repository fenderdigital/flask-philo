from unittest.mock import Mock
from flaskutils import app
from flaskutils.test import FlaskTestCase


import json
import pytest


class TestAppCase(FlaskTestCase):
    def setup(self):
        self.client = app.test_client()
        self.json_request_headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        super(TestAppCase, self).setup()

    def test_get(self):
        rclient = self.redis_pool.connections['DEFAULT']
        data = {'key1': 1}
        rclient.set('key1', json.dumps(data))
        result = self.client.get('/redis/key1')
        assert 200 == result.status_code
        data2 = json.loads(result.get_data().decode('utf-8'))
        assert data == data2

    def test_post(self):
        result = self.client.get('/redis/key1')
        assert 404 == result.status_code
        data = {'key1': 1}
        result = self.client.post(
            '/redis/key1',
            data=json.dumps(data),
            headers=self.json_request_headers
        )
        assert 201 == result.status_code
        rclient = self.redis_pool.connections['DEFAULT']
        assert '{"key1": 1}' == rclient.get('key1').decode('utf-8')

        result = self.client.get('/redis/key1')
        assert 200 == result.status_code
        data2 = json.loads(result.get_data().decode('utf-8'))
        assert data == data2
