from flaskutils.test import FlaskTestCase
from flaskutils.db.postgresql.connection import get_pool

from unittest.mock import Mock

from tests.test_app.models import User
from tests.test_app.serializers import GetUserSerializer, PostUserSerializer


class TestDBAccess(FlaskTestCase):
    def test_connection_open(self):
        """
        checks if connection is open
        """
        pool = get_pool()
        result = pool.connections['DEFAULT'].session.execute('SELECT 19;')
        assert result.fetchone()[0] == 19
        pool.connections['DEFAULT'].session.close()

    def test_get_insert(self):
        pool = get_pool()
        assert 0 == User.objects.count()
        user = User(
            username='username1', email='email1@email.com', password='123')
        user.add()
        pool.commit()
        assert 1 == User.objects.count()

    def test_model_to_json(self):
        pool = get_pool()
        assert 0 == User.objects.count()
        user = User(
            username='username1', email='email1@email.com', password='123')
        user.add()
        pool.commit()

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
        data = PostUserSerializer(request=request).to_json()
        user_model = User(**data)
        assert user_dict['username'] == user_model.username
        assert user_model.email == user_dict['email']
