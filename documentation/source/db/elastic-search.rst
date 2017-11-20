Flask-Philo Elastic Search Connector
========================================

Elasticsearch is a distributed, RESTful search and analytics engine.


Where's Elastic Search on Flask-Philo project
-----------------------------------------------

Elastic Search Redis client and connector can be found at:

https://github.com/Riffstation/flask-philo/tree/dev/flask_philo/db/elasticsearch


Importing Elastic Search Connection
------------------------------------

To import Elastic Search connection, just do:

::

 from flask_philo.db.elasticsearch.connection import get_pool as get_el_pool

 elasticsearch_pool = get_el_pool()
 client = elasticsearch_pool.connections['DEFAULT']

Setting up your development config file
---------------------------------------

In your flask app, in the file ``src/config/development/py``, insert the following piece of code:

::

    DATABASES = {
        'ELASTICSEARCH': {
            'DEFAULT': {
                'HOSTS': [
                    {'host': 'localhost', 'port': '9200'}
                ]
            }
        }
    }



Create an Index
----------------

::

 elasticsearch_pool.create_index('test-index')



Indexing data on Elastic Search
----------------------------------

You can use the following syntax to add data to Elastic Search:

::

    doc = {
        'author': 'kimchy',
        'text': 'Elasticsearch: cool. bonsai cool.',
        'timestamp': datetime.now(),
    }

    elasticsearch_pool.index(
        index="test-index", doc_type='tweet', id=1, body=doc)



Bulk Indexing
------------------------------------------


::

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

    elasticsearch_pool.bulk_index(
        index='test-index', doc_type='logs', data=documents)

    assert len(documents) == elasticsearch_pool.count('test-index')



Searching
------------------

::

    results = elasticsearch_pool.search(index='test-index')
    assert len(docs) == len(results['hits']['hits'])

    body = {
        'size': 2
    }
    results = elasticsearch_pool.search(
        index='test-index', body=body)
    assert 2 == len(results['hits']['hits'])

    body = {
        'query': {
            'match': {'msg': 'user'}
        }
    }

    results = elasticsearch_pool.search(
        index='test-index', doc_type='logs', body=body)

    assert len(docs) == len(results['hits']['hits'])

    body = {
        'query': {
            'match': {'msg': 'table'}
        }
    }
    results = elasticsearch_pool.search(
        index='test-index', doc_type='logs', body=body)
    assert 2 == len(results['hits']['hits'])

    body = {
        'query': {
            'bool': {
                'must': {
                    'match': {'msg': 'user update record'},
                },
                'must_not': {
                    'match': {'msg': 'create'}
                }

            }
        }
    }
    results = elasticsearch_pool.search(
        index='test-index', doc_type='logs', body=body)



Deleting Documents
------------------------------

::

    elasticsearch_pool.index(
        index="test-index", doc_type='tweet', id=1, body={'hi': 'hello'})
    elasticsearch_pool.delete('test-index', 'tweet', 1)
