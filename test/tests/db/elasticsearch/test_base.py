from datetime import datetime
from elasticsearch.exceptions import NotFoundError
from flaskutils.test import FlaskTestCase

import pytest
import time


class TestDBAccess(FlaskTestCase):
    def test_connection(self):
        client = self.elasticsearch_pool.connections['DEFAULT']
        assert client.ping() is True

    def test_create_index(self):
        client = self.elasticsearch_pool.connections['DEFAULT']
        assert {} == client.get_alias()
        client.create_index('my-test')
        assert 'my-test' in client.get_alias()

    def test_insert_doc(self):

        doc = {
            'author': 'kimchy',
            'text': 'Elasticsearch: cool. bonsai cool.',
            'timestamp': datetime.now(),
        }

        self.elasticsearch_pool.create_index('test-index')
        with pytest.raises(NotFoundError):
            self.elasticsearch_pool.get(
                index="test-index", doc_type='tweet', id=1)
        assert 0 == self.elasticsearch_pool.count('test-index')

        self.elasticsearch_pool.index(
            index="test-index", doc_type='tweet', id=1, body=doc)
        time.sleep(1)
        assert 1 == self.elasticsearch_pool.count('test-index')
        res = self.elasticsearch_pool.get(
                index="test-index", doc_type='tweet', id=1)
        assert '_source' in res
        assert res['_source'].keys() == doc.keys()
        assert res['_source']['author'] == 'kimchy'

    def test_delete_doc(self):
        self.elasticsearch_pool.create_index('test-index')
        self.elasticsearch_pool.index(
            index="test-index", doc_type='tweet', id=1, body={'hi': 'hello'})
        self.elasticsearch_pool.get(
                index="test-index", doc_type='tweet', id=1)
        self.elasticsearch_pool.delete('test-index', 'tweet', 1)
        with pytest.raises(NotFoundError):
            self.elasticsearch_pool.get(
                index="test-index", doc_type='tweet', id=1)

    def get_documents(self):
        documents = [
            {
                'id': 1, 'msg': 'user 1 create record from machine 3',
                'timestamp': datetime.now(),
            },

            {
                'id': 2, 'msg': 'user 2 update record from machine 6',
                'timestamp': datetime.now()
            },

            {
                'id': 3, 'msg': 'user 1 create table server 2',
                'timestamp': datetime.now()
            },
            {
                'id': 4, 'msg': 'user 1 create table server 2',
                'timestamp': datetime.now()
            },

        ]
        return documents

    def test_bulk_index(self):
        self.elasticsearch_pool.create_index('test-index')
        assert 0 == self.elasticsearch_pool.count('test-index')
        documents = self.get_documents()
        self.elasticsearch_pool.bulk_index(
            index='test-index', doc_type='logs', data=documents)
        time.sleep(1)
        assert len(documents) == self.elasticsearch_pool.count('test-index')

    def test_search(self):
        self.elasticsearch_pool.create_index('test-index')
        docs = self.get_documents()
        self.elasticsearch_pool.bulk_index(
            index='test-index', doc_type='logs', data=docs)
        time.sleep(1)
        results = self.elasticsearch_pool.search(index='test-index')
        assert len(docs) == len(results['hits']['hits'])

        body = {
            'size': 2
        }
        results = self.elasticsearch_pool.search(
            index='test-index', body=body)
        assert 2 == len(results['hits']['hits'])
        body = {
            'query': {
                'match':
                 {'msg': 'user 1 create table server 2'}
            }
        }

        results = self.elasticsearch_pool.search(
            index='test-index', body=body)
        print(results)
        #import ipdb; ipdb.set_trace()

REPO_ACTIONS = [
    {'_type': 'repos', '_id': 'elasticsearch', '_source': {
        'owner': {'name': 'Shay Bannon', 'email': 'kimchy@gmail.com'},
        'created_at': datetime(2010, 2, 8, 15, 22, 27),
        'tags': ['search', 'distributed', 'lucene'],
        'description': 'You know, for search.'}
    },

    {'_type': 'repos', '_id': 'elasticsearch-py', '_op_type': 'update', 'doc': {
        'owner': {'name': u'Honza Král', 'email': 'honza.kral@gmail.com'},
        'created_at': datetime(2013, 5, 1, 16, 37, 32),
        'tags': ['elasticsearch', 'search', 'python', 'client'],
        'description': 'For searching snakes.'}
    },
]
