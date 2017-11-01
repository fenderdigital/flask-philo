Flask-Philo Redis Connector
============================

Redis is a fast key-value store and can be used to support high performance scalable web
applications.


Where's Redis on Flask-Philo project
----------------------------------------

Flask-Philo Redis client and connector can be found at:

https://github.com/Riffstation/flask-philo/tree/dev/flask_philo/db/redis


Importing Redis Connection
----------------------------

To import redis connection, just do:

::

 from flask_philo.db.redis.connection import get_pool as get_redis_pool

 redis_pool = get_redis_pool()
 client = redis_pool.connections['DETAULT']

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



To add or update data on Redis
------------------------------

You can use the following syntax to add data to Redis:

::

    from flask_philo.db.redis.connection import get_pool as get_redis_pool

    redis_pool = get_redis_pool()
    client = redis_pool.connections['DETAULT']
    client.set('your_key', data_set)


To retrieve data from Redis
---------------------------

You can use the following syntax to add data from Redis:

::

    from flask_philo.db.redis.connection import get_pool as get_redis_pool

    redis_pool = get_redis_pool()
    client = redis_pool.connections['DETAULT']
    # retrieving data
    client.get('your_key')


You have a set of operations that can be done on Redis. You can find it here:

https://github.com/Riffstation/flask_philo/tree/dev/flask_philo/db/redis


You can also operate direct on Redis server, for example, to retrieve a value by giving its proper key.
