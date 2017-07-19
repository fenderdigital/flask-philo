from flaskutils.test import FlaskTestCase
from flaskutils.db.postgresql.connection import get_pool

from .models import Genre


class TestMultiDBModel(FlaskTestCase):
    def setup(self):
        super(TestMultiDBModel, self).setup()
        self.pool = get_pool()

    def test_muti_crud(self):

        rock = Genre(name='Rock', description='db1')
        rock.add(connection_name='DEFAULT')
        self.pool.commit()

        assert 1 == Genre.objects.count(connection_name='DEFAULT')
        assert 0 == Genre.objects.count(connection_name='DB2')

        rock2 = Genre(name='Rock', description='db2')
        rock2.add(connection_name='DB2')
        self.pool.commit()

        assert 1 == Genre.objects.count(connection_name='DB2')

        r1 = Genre.objects.get(connection_name='DB2', name='Rock')
        r2 = Genre.objects.get(connection_name='DEFAULT', name='Rock')

        assert r1.description != r2.description

        rock.delete()
        self.pool.commit()
        assert 0 == Genre.objects.count(connection_name='DEFAULT')

        l1 = list(Genre.objects.filter_by(connection_name='DEFAULT'))
        l2 = list(Genre.objects.filter_by(connection_name='DB2'))

        assert 0 == len(l1)
        assert 1 == len(l2)
