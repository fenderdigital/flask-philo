from flaskutils.test import FlaskTestCase
from flaskutils.db.postgresql.connection import get_pool
from flaskutils.db.postgresql.types import PasswordHash


class TestDBAccess(FlaskTestCase):
    def test_connection_open(self):
        """
        checks if connection is open
        """
        pool = get_pool()
        result = pool.connections['DEFAULT'].session.execute('SELECT 19;')
        assert result.fetchone()[0] == 19
        pool.connections['DEFAULT'].session.close()


class TestPassword(FlaskTestCase):
    def test_password_equal(self):
        a = PasswordHash.new('123', 12)
        assert a == '123'
        assert a != '1232'
