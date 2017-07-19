from flaskutils.exceptions import AuthenticationError
from flaskutils.test import FlaskTestCase

from tests.test_app.models import User

import pytest


class TestAuthUser(FlaskTestCase):
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


class TestBasicAuth(FlaskTestCase):

    def test_requires_auth__endpoint_without_valid_credentials(self):
        result = self.client.get('/basic_auth', headers={
            'Authorization': 'Basic dXNlcjpwYXNz'})
        assert 401 == result.status_code

    def test_requires_auth_endpoint_with_valid_credentials(self):
        result = self.client.get('/basic_auth', headers={
            'Authorization': 'Basic dXNlcm5hbWU6cGFzc3dvcmQ='})
        assert 200 == result.status_code
