Unit Tests
=============================================

Writing Unit Tests with Flask-Philo
--------------------

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

To run all Unit Tests for a Flask-Philo app, use the following console command:

::

    python3 manage.py test



To execute *only* the Unit Tests from one **source file**, use the ``--q <test_source.py>`` argument:

::

    python3 manage.py test --q tests/test_db.py


To execute *only* the tests from one **class** :


::

    python3 manage.py test --q tests/test_db.py::TestDBAccess


To execute a single specific unit test :

::

    python3 manage.py test --q tests/test_db.py::TestDBAccess::test_create_index
