from .client import ElasticSearchClient

import elasticsearch
import sys


class ElasticSearchPool:
    """
    """
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state

    def ping(self, db='DEFAULT'):
        return self.connections[db].ping()

    def get_alias(self, db='DEFAULT', name=None):
        return self.connections[db].get_alias(name=name)

    def create_index(self, name, db='DEFAULT'):
        return self.connections[db].create_index(name)

    def get(self, db='DEFAULT', index=None, doc_type=None, id=None):
        return self.connections[db].get(index=index, doc_type=doc_type, id=id)

    def delete_index(self, index, name, db='DEFAULT'):
        return self.connections[db].delete_index(index, name)

    def delete(self, index, doc_type, id, db='DEFAULT'):
        return self.connections[db].delete(index, doc_type, id)

    def index(
            self, db='DEFAULT', index=None, doc_type=None, id=None, body=None):
        return self.connections[db].index(
            index=index, doc_type=doc_type, id=id, body=body)

    def count(self, index, db='DEFAULT'):
        return self.connections[db].count(index)

    def search(self, db='DEFAULT', **kwargs):
        return self.connections[db].search(**kwargs)

    def bulk_index(self, db='DEFAULT', data=None, index=None, doc_type=None):
        self.connections[db].bulk_index(
            data=data, index=index, doc_type=doc_type)

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
            v.flush()


el_pool = ElasticSearchPool()
el_pool.connections = {}


def get_pool():
    return el_pool


def init_db_conn(connection_name, HOSTS=None):
    """
    Initialize a redis connection by each connection string
    defined in the configuration file
    """
    el = elasticsearch.Elasticsearch(hosts=HOSTS)
    el_pool.connections[connection_name] = ElasticSearchClient(el)


def initialize(g, app):
    """
    If elastic search connection parameters are defined in configuration
    params a session will be created
    """

    if 'DATABASES' in app.config and\
            'ELASTICSEARCH' in app.config['DATABASES']:

        # Initialize connections for console commands
        for k, v in app.config['DATABASES']['ELASTICSEARCH'].items():
            init_db_conn(k, **v)

        @app.before_request
        def before_request():
            """
            Assign elastic search connection pool to the global
            flask object at the beginning of every request
            """
            for k, v in app.config['DATABASES']['ELASTICSEARCH'].items():
                init_db_conn(k, **v)
            g.elasticsearch_pool = el_pool

        if 'test' not in sys.argv:
            @app.teardown_request
            def teardown_request(exception):
                pool = getattr(g, 'el_pool', None)
                if pool is not None:
                    pool.close()
