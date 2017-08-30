from .client import RedisClient

import json
import redis
import sys


class RedisPool:
    """
    """
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state

    def ping(self, db='DEFAULT'):
        return self.connections[db].ping()

    def set_json(self, k, v, db='DEFAULT'):
        jval = json.dumps(v)
        self.set(k, jval)

    def set(self, k, v, db='DEFAULT'):
        self.connections[db].set(k, v)

    def delete(self, k, db='DEFAULT'):
        self.connections[db].delete(k)

    def get_json(self, k, db='DEFAULT', encode='utf-8'):
        val = self.get(k, db=db)
        if val is not None:
            return json.loads(val.decode(encode))
        else:
            return {}

    def get(self, k, db='DEFAULT'):
        return self.connections[db].get(k)

    def close(self, db=None):
        if db is None:
            for k, v in self.connections.items():
                v.close()
            self.connections = {}
        else:
            v = self.connections[db]
            v.close()
            del self.connections[db]

    def flushall(self):
        for k, v in self.connections.items():
            v.flushdb()


redis_pool = RedisPool()
redis_pool.connections = {}


def get_pool():
    return redis_pool


def init_db_conn(
        connection_name, HOST=None, PORT=None, DB=None, PASSWORD=None):
    """
    Initialize a redis connection by each connection string
    defined in the configuration file
    """
    rpool = redis.ConnectionPool(
        host=HOST, port=PORT, db=DB, password=PASSWORD)
    r = redis.Redis(connection_pool=rpool)
    redis_pool.connections[connection_name] = RedisClient(r)


def initialize(g, app):
    """
    If redis connection parameters are defined in configuration params a
    session will be created
    """

    if 'DATABASES' in app.config and 'REDIS' in app.config['DATABASES']:

        # Initialize connections for console commands
        for k, v in app.config['DATABASES']['REDIS'].items():
            init_db_conn(k, **v)

        @app.before_request
        def before_request():
            """
            Assign redis connection pool to the global
            flask object at the beginning of every request
            """
            for k, v in app.config['DATABASES']['REDIS'].items():
                init_db_conn(k, **v)
            g.redis_pool = redis_pool

        if 'test' not in sys.argv:
            @app.teardown_request
            def teardown_request(exception):
                pool = getattr(g, 'redis_pool', None)
                if pool is not None:
                    pool.close()
