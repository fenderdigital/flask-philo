from flaskutils.exceptions import AuthenticationError
from flaskutils.test import ModelTestCase, TransactionalTestCase

from tests.test_app.models import User

import json
import pytest


class TestAuthUser(ModelTestCase):
    def test_invalid_password(self):
        user = User(
            username='user', email='user@user.com', password='123')
        user.add()

        with pytest.raises(AuthenticationError) as excinfo:
            User.authenticate(
                username='user', email='user@user.com', password='12345')
        assert 'invalid credentials' in str(excinfo.value)

    def test_invalid_username(self):
        with pytest.raises(AuthenticationError) as excinfo:
            User.authenticate(
                username='not exists', email='user@user.com', password='12345')
        assert 'invalid credentials' in str(excinfo.value)

    def test_valid_password(self):
        user = User(
            username='user', email='user@user.com', password='123')
        user.add()

        user2 = User.authenticate(
            username='user', email='user@user.com', password='123')

        assert user.password == user2.password
        assert user.id == user2.id


class TestAuth(TransactionalTestCase):

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

    def test_successful_login(self):
        assert (
            'localhost.local' not in
            self.client.cookie_jar._cookies)
        user = User(
            username='user', email='user@user.com',
            password='123', is_active=True)
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
        assert (
            'session' in
            self.client.cookie_jar._cookies['localhost.local']['/'])

    def test_invalid_password(self):
        assert (
            'localhost.local' not in
            self.client.cookie_jar._cookies)
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

    def test_login_required(self):
        result = self.client.get(
            '/protected',
            headers=self.json_request_headers
        )

        assert 401 == result.status_code
        user = User(
            username='user', email='user@user.com',
            password='123', is_active=True)
        user.add()
        credentials = {
            'username': 'user', 'email': 'user@user.com', 'password': '123'}
        result = self.client.post(
            '/login',
            data=json.dumps(credentials),
            headers=self.json_request_headers
        )
        result = self.client.get(
            '/protected',
            headers=self.json_request_headers
        )
        assert 200 == result.status_code

    def test_logout(self):
        assert (
            'localhost.local' not in
            self.client.cookie_jar._cookies)
        user = User(
            username='user', email='user@user.com',
            password='123', is_active=True)
        user.add()
        credentials = {
            'username': 'user', 'email': 'user@user.com', 'password': '123'}
        result = self.client.post(
            '/login',
            data=json.dumps(credentials),
            headers=self.json_request_headers
        )
        assert (
            'session' in
            self.client.cookie_jar._cookies['localhost.local']['/'])

        result = self.client.get(
            '/protected',
            headers=self.json_request_headers
        )
        assert 200 == result.status_code
        result = self.client.post(
            '/logout',
            data=json.dumps(credentials),
            headers=self.json_request_headers
        )
        assert 200 == result.status_code

        result = self.client.get(
            '/protected',
            headers=self.json_request_headers
        )
        assert 401 == result.status_code


class TestBasicAuth(TransactionalTestCase):

    def test_requires_auth__endpoint_without_valid_credentials(self):
        result = self.client.get('/basic_auth', headers={
            'Authorization': 'Basic dXNlcjpwYXNz'})
        assert 401 == result.status_code

    def test_requires_auth_endpoint_with_valid_credentials(self):
        result = self.client.get('/basic_auth', headers={
            'Authorization': 'Basic dXNlcm5hbWU6cGFzc3dvcmQ='})
        assert 200 == result.status_code
