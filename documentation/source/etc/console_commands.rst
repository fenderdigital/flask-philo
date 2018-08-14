Console Commands
=============================================

Flask-Philo provides a number of console commands to manage core app services and common tasks (e.g. ``runserver``, ``syncdb``, ``test``, etc).

However, Flask-Philo also allows us to *extend* this set of console commands with our own *custom* commands.
This let us write custom utilities and tools that take advantage of the inherent features of a Flask-Philo application: ORM mapping, app Views, app Models, DB config, etc)

Running Console Commands
--------------------

In general, we use the ``manage.py`` program as our starting point for launching console commands. Many useful commands are already included as part of Flask-Philo:

::

    $ python3 manage.py runserver
    $ python3 manage.py test
    $ python3 manage.py syncdb


Writing Custom Console Commands
--------------------
