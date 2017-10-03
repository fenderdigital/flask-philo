FlaskUtils Redis Connector
==========================

What's Redis about
------------------

Redis is a fast key-value store and can be used to support high performance scalable web applications.


Where's Redis on FlaskUtils project
-----------------------------------

FlaskUtils Redis client and connector can be found at:

https://github.com/Riffstation/flaskutils/tree/dev/flaskutils/db/redis


Importing Redis Connection
--------------------------

To import redis connection, just do:

::

 from flaskutils.db.redis.connection import *



Setting up your development config file
---------------------------------------

In your flask app, in the file ``src/config/development/py``, insert the following piece of code:

::

 DATABASES = {
     # existing database connections would be here
     'REDIS': {
         'DEFAULT': { # Your cluster connection name
             'HOST': '<your_host>', #By default will be 127.0.0.1
             'PORT': <your_port>, # By default redis uses 6379
             'DB': <your_db_name>, # By default redis uses DB:0
             'PASSWORD': '<your_password>' # In case your redis cluster is with auth
         }
     }
 }

To initialize a Redis connection
--------------------------------

Once you have you Redis db connection set, you can initialize it in this way:

::

 from flaskutils.db.redis.connection import get_pool

 redis_pool = get_pool()
 client = redis_pool.connections['DETAULT']


To add or update data on Redis
------------------------------

You can use the following syntax to add data to Redis:

::

 from flaskutils.db.redis.connection import get_pool

 def run(**kwags):
    data_set = [
        # data you need to set up on redis
    ]

    redis_pool = get_pool()
    # setting up a connection
    client = redis_pool.connections['DETAULT']
    # adding/update data
    client.set('your_key', data_set)


To retrieve data from Redis
---------------------------

You can use the following syntax to add data from Redis:

::

 from flaskutils.db.redis.connection import get_pool

 redis_pool = get_pool()

 # setting up a connection
 client = redis_pool.connections['DETAULT']
 # retrieving data
 client.get('your_key')


You have a set of operations that can be done on Redis. You can find it here:

https://github.com/Riffstation/flaskutils/tree/dev/flaskutils/db/redis


You can also operate direct on Redis server, for example, to retrieve a value by giving its proper key.
