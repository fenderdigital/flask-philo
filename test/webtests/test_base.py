from datetime import date, datetime
from unittest.mock import Mock

from flaskutils import app
from flaskutils import utils
from flaskutils.test import TestApiCase
from flask import Flask

from jsonschema import ValidationError
from .serializers import PostUserSerializer, PutUserSerializer

import json
import pytest


class TestAppCase(object):
    def setup(self):
        self.client = app.test_client()
        self.json_request_headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_app_instanciate(self):
        """
        Test if the flask app was correctly instanciated
        """
        assert isinstance(app, Flask)
        assert 'run_tests' == app.name

    def test_render_html(self):
        """
        Makes a HTTP GET REQUEST AND GETS html
        """
        result = self.client.get('/')
        assert 200 == result.status_code
        assert b'<h1>hello world!!!</h1>' == result.get_data()


class TestValidators(object):
    def setup(self):
        self.request = Mock()

    def test_validate_simple_json(self):
        user_dict = {
            'id': 1, 'username': 'userupdated',
            'email': 'email@test.com', 'last_login': '2016-06-21 08:00:00'}
        self.request.json = user_dict
        user_obj = PutUserSerializer(request=self.request)
        assert user_obj.id == user_dict['id']
        assert user_obj.username == user_dict['username']
        assert user_obj.email == user_dict['email']

    def test_validate_invalid_email(self):
        user_dict = {'id': 1, 'username': 'userupdated', 'email': 'email'}
        self.request.json = user_dict
        with pytest.raises(ValidationError) as excinfo:
            PutUserSerializer(request=self.request)
        assert "'email' is not a 'email'" in str(excinfo.value)

    def test_validate_invalid_extra_field(self):
        user_dict = {
            'id': 1, 'username': 'userupdated',
            'email': 'email@email.com', 'extra': 'danger'
        }
        self.request.json = user_dict
        with pytest.raises(ValidationError) as excinfo:
            PutUserSerializer(request=self.request)
        assert "'extra' was unexpected)" in str(excinfo.value)

    def test_serialize_from_model(self):
        user_model = Mock()
        user_model.email = 'email@email.com'
        user_model.username = 'username'
        user_model.last_login = datetime(2016, 6, 21, 8, 15)
        user_model.birthday = date(2016, 6, 21)
        user_serializer = PostUserSerializer(model=user_model)
        json_obj = user_serializer.to_json()
        assert json_obj['birthday'] == '2016-06-21'
        assert json_obj['last_login'] == '2016-06-21 08:15:00'


class TestApiRequest(TestApiCase):

    def test_get_resource(self):
        """
        Get a Rest resource in json format
        """
        result = self.client.get('/users/1')
        assert 200 == result.status_code
        data = json.loads(result.get_data().decode('utf-8'))
        assert 'username' in data
        assert 'id' in data

    def test_get_resource_list(self):
        """
        Get a list of rest resources
        """
        result = self.client.get('/users')
        assert 200 == result.status_code
        data = json.loads(result.get_data().decode('utf-8'))
        assert len(data) == 2
        assert 'username' in data[0]
        assert 'id' in data[0]

    def test_post_resource(self):
        """
        Test A valid
        """

    def test_put_resource(self):
        """
        Test A valid put request
        """
        user = {'id': 1, 'username': 'userupdated', 'email': 'email@test.com'}
        response = self.client.put(
            '/users/1',
            data=json.dumps(user),
            headers=self.json_request_headers
        )

    def test_password_authentication(self):
        """
        valid  username and password  authentication backend
        """

    def test_token_authentication(self):
        """
        test api token authentication backend
        """

    def test_unautorized_request(self):
        """
        invalid request, user unauthorized
        """

    def test_post_rest_request(self):
        """
        create a new resource with a json request
        """

    def test_put_rest_request(self):
        """
        updating a resource using put
        """

    def test_patch_rest_request(self):
        """
        updating a resource using put
        """

    def test_delete_rest_request(self):
        """
        deleting a resource using put
        """
