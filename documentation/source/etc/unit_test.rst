Writing Unit Test with Flask-Philo
=============================================

Flask-Philo supports unit tests. All you have to do is 
create a class insised ``tests`` directory in your project
that extends ``flask_philo.test.FlaskTestCase``.

E.g.

::

    from datetime import datetime
    from elasticsearch.exceptions import NotFoundError
    from flask_philo.test import FlaskTestCase

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



Running Unit Tests
--------------------

  ::

    python3 manage.py test



You can execute the tests from one file by using the ``q`` parameter:

::

    python3 manage.py test --q tests/test_db.py


You can execute the tests from one class by running:


::

    python3 manage.py test --q tests/test_db.py::TestDBAccess


 You can execute a specific unit test by running:

::

    python3 manage.py test --q tests/test_db.py::TestDBAccess::test_create_index
