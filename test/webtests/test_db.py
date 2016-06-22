from flaskutils.test import TransactionalTestCase
from pgsqlutils.base import Session

from .models import User
from .serializers import GetUserSerializer


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

        user2 = User.objects.get(user.id)
        serializer = GetUserSerializer(model=user2)
        json_model = serializer.to_json()
        assert user2.id == json_model['id']
        assert user2.username == json_model['username']
        assert user2.email == json_model['email']
        assert 'password' not in json_model
