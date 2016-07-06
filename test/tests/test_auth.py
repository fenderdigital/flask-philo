from flaskutils import app
from flaskutils.test import TransactionalTestCase

from tests.test_app.models import User

import json


class TestAuth(TransactionalTestCase):
    def setup(self):
        self.client = app.test_client()
        self.json_request_headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_401_unauthorized(self):
        """
        Get and error when credentials not provided
        """
        result = self.client.post('/login')
        assert 401 == result.status_code


    def test_401_password_username_missing(self):
        """
        Error when username or password are missing
        """
        user = User(
            username='user', email='user@user.com', password='123')
        user.add()

        credentials = {'username': 'user', 'email': 'user@user.com'}
        result = self.client.post(
            '/login',
            data=json.dumps(credentials),
            headers=self.json_request_headers
        )
        assert 401 == result.status_code
        data = json.loads(result.get_data().decode('utf-8'))
        assert 'msg' in data
        assert "'password' is a required property" == data['msg']

        credentials = {'username': 'username', 'email': 'user@user.com'}
        result = self.client.post(
            '/login',
            data=json.dumps(credentials),
            headers=self.json_request_headers
        )
        assert 401 == result.status_code
        data = json.loads(result.get_data().decode('utf-8'))
        assert 'msg' in data
        assert "'password' is a required property" == data['msg']

    def test_401_unexisting_user(self):
        credentials = {
            'username': 'user', 'email': 'user@user.com', 'password': '123'}
        result = self.client.post(
            '/login',
            data=json.dumps(credentials),
            headers=self.json_request_headers
        )
        assert 401 == result.status_code
        data = json.loads(result.get_data().decode('utf-8'))
        assert 'msg' in data
        assert "invalid credentials" == data['msg']

    def test_successfull_login(self):
        user = User(
            username='user', email='user@user.com', password='123')
        user.add()
        credentials = {
            'username': 'user', 'email': 'user@user.com', 'password': '123'}
        result = self.client.post(
            '/login',
            data=json.dumps(credentials),
            headers=self.json_request_headers
        )
        assert 200 == result.status_code
        data = json.loads(result.get_data().decode('utf-8'))
        assert 'username' in data
        assert 'user' == data['username']

    def test_invalid_password(self):
        user = User(
            username='user', email='user@user.com', password='123')
        user.add()
        credentials = {
            'username': 'user', 'email': 'user@user.com', 'password': '1233'}
        result = self.client.post(
            '/login',
            data=json.dumps(credentials),
            headers=self.json_request_headers
        )
        assert 401 == result.status_code
        data = json.loads(result.get_data().decode('utf-8'))
        assert 'msg' in data
        assert "invalid credentials" == data['msg']