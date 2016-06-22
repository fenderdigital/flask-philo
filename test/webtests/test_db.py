from flaskutils.test import TransactionalTestCase
from pgsqlutils.base import init_db_conn, syncdb, Session
from .models import User

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
