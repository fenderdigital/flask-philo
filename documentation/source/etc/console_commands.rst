Console Commands
=============================================

Flask-Philo provides a number of console commands to manage core app services and common tasks (e.g. ``runserver``, ``syncdb``, ``test``, etc).

However, Flask-Philo also allows us to *extend* this set of console commands with our own *custom* commands.
This let us write custom utilities and tools that take advantage of the inherent features of a Flask-Philo application: ORM mapping, View/Model architecture, DB config, etc)

Running Console Commands
--------------------


::

    python3 manage.py test



To execute *only* the tests from one **source file**, use the ``--q`` parameter:

::

    python3 manage.py test --q tests/test_db.py


To execute *only* the tests from one **class** :


::

    python3 manage.py test --q tests/test_db.py::TestDBAccess


To execute a single specific unit test :

::

    python3 manage.py test --q tests/test_db.py::TestDBAccess::test_create_index


Writing Custom Console Commands
--------------------
