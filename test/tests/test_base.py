from datetime import date, datetime
from unittest.mock import Mock

from flaskutils import app
from flaskutils.test import TransactionalTestCase
from flask import Flask
from jsonschema import ValidationError
from pgsqlutils.base import Session

from tests.test_app.models import User
from tests.test_app.serializers import (
    PostUserSerializer, PutUserSerializer, UUIDSerializer)

import json
import pytest
import uuid


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
        assert 'manage' == app.name

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

    def test_serialize_uuid(self):
        data = {'key': str(uuid.uuid4())}
        serializer = UUIDSerializer(data=data)
        jdata = serializer.to_json()
        assert str(data['key']) == jdata['key']


class TestApiRequest(TransactionalTestCase):

    def test_get_resource(self):
        """
        Get a Rest resource in json format
        """
        user = User(
            username='username1', email='email1@email.com', password='123')
        user.add()

        user2 = User(
            username='username2', email='email2@email.com', password='123')
        user2.add()

        result = self.client.get('/users/{}'.format(user.id))
        assert 200 == result.status_code
        data = json.loads(result.get_data().decode('utf-8'))
        assert 'username' in data
        assert 'id' in data
        assert user.id == data['id']

    def test_get_resource_list(self):
        """
        Get a list of rest resources
        """
        user = User(
            username='username1', email='email1@email.com', password='123')
        user.add()

        user2 = User(
            username='username2', email='email2@email.com', password='123')
        user2.add()
        result = self.client.get('/users')
        assert 200 == result.status_code
        data = json.loads(result.get_data().decode('utf-8'))
        assert len(data) == 2
        assert 'username' in data[0]
        assert 'id' in data[0]
        assert user.id == data[0]['id']
        assert user2.id == data[1]['id']

    def test_post_resource(self):
        """
        Test A valid
        """
        assert 0 == User.objects.count()
        user = {
            'username': 'user', 'email': 'email@test.com', 'password': '123'}
        response = self.client.post(
            '/users',
            data=json.dumps(user),
            headers=self.json_request_headers
        )
        assert 1 == User.objects.count()
        assert 201 == response.status_code
        data = json.loads(response.get_data().decode('utf-8'))
        user2 = User.objects.filter_by()[0]
        assert data['id'] == user2.id

    def test_put_resource(self):
        """
        Test A valid put request
        """
        user = User(
            username='username1', email='email1@email.com', password='123')
        user.add()
        Session.commit()
        data = {
            'id': user.id, 'username': 'updatedusername',
            'email': user.email, 'password': '123'}

        result = self.client.put(
            '/users/{}'.format(user.id),
            data=json.dumps(data),
            headers=self.json_request_headers
        )
        data = json.loads(result.get_data().decode('utf-8'))
        user2 = User.objects.get(id=user.id)

        assert 200 == result.status_code
        assert 1 == User.objects.count()
        assert user.id == user2.id and user2.id == data['id']

    def test_delete_resource(self):
        """
        deleting a resource using delete
        """
        user = User(
            username='username1', email='email1@email.com', password='123')
        user.add()
        Session.commit()
        assert 1 == User.objects.count()
        result = self.client.delete(
            '/users/{}'.format(user.id),
            headers=self.json_request_headers
        )
        assert 200 == result.status_code
        assert 0 == User.objects.count()
