from datetime import date, datetime
from unittest.mock import Mock
from jsonschema import ValidationError
from decimal import Decimal
import pytest
import uuid

from tests.test_app.serializers import (
    PostUserSerializer, PutUserSerializer, UUIDSerializer, DecimalSerializer)


class TestSerializer(object):
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

    def test_serialize_decimal(self):
        data = {'credit_score': '3.456677'}
        serializer = DecimalSerializer(data=data)
        assert isinstance(serializer.credit_score, Decimal)
        assert round(
            Decimal(3.456677), 5) == round(serializer.credit_score, 5)
        jdata = serializer.to_json()
        assert jdata['credit_score'] == '3.456677'
