from flaskutils.test import FlaskTestCase


class TestDBAccess(FlaskTestCase):
    def test_connection(self):
        client = self.redis_pool.connections['DEFAULT']
        assert client.ping() is True

    def test_crud(self):
        client = self.redis_pool.connections['DEFAULT']
        assert client.get('key1') is None
        client.set('key1', 1)
        assert '1' == client.get('key1').decode('utf-8')
        client.set('key1', 2)
        assert '2' == client.get('key1').decode('utf-8')

        client.flushdb()
        assert client.get('key1') is None

        client.set('key1', 1)
        client.set('key2', 2)

        assert '1' == client.get('key1').decode('utf-8')
        client.delete('key1')
        assert client.get('key1') is None
        assert '2' == client.get('key2').decode('utf-8')

    def test_list(self):
        items = [1, 2, 3]
        client = self.redis_pool.connections['DEFAULT']
        client.set('items', items)
        assert '[1, 2, 3]' == client.get('items').decode('utf-8')
