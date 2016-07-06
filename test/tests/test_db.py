from flaskutils.test import TransactionalTestCase
from pgsqlutils.base import Session

from unittest.mock import Mock

from .models import User
from .serializers import GetUserSerializer, PostUserSerializer


class TestDBAccess(TransactionalTestCase):
    def test_connection_open(self):
        """
        checks if connection is open
        """
        result = Session.execute('SELECT 19;')
        assert result.fetchone()[0] == 19
        Session.close()

    def test_get_insert(self):
        assert 0 == User.objects.count()
        user = User(
            username='username1', email='email1@email.com', password='123')
        user.add()
        assert 1 == User.objects.count()

    def test_model_to_json(self):
        user = User(
            username='username1', email='email1@email.com', password='123')
        user.add()

        user2 = User.objects.get(id=user.id)
        serializer = GetUserSerializer(model=user2)
        json_model = serializer.to_json()
        assert user2.id == json_model['id']
        assert user2.username == json_model['username']
        assert user2.email == json_model['email']
        assert 'password' not in json_model

    def test_serializer_to_model(self):

        request = Mock()
        user_dict = {
            'username': 'userupdated', 'password': '123',
            'email': 'email@test.com'}
        request.json = user_dict
        user_serializer = PostUserSerializer(request=request)
        user_model = User(serializer=user_serializer)
        assert user_dict['username'] == user_model.username
        assert user_model.email == user_dict['email']
