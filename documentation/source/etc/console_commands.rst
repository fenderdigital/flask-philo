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

We can extend our application's set of utility commands by adding Python programs to the ``src/console_commands`` directory. For example, when we save the following code to ``src/console_commands/count_users``, we now have a simple console command that counts our application's Users, and outputs it to the console:

::
    #!/usr/bin/env python
    """
    Example console command that outputs a count of all User objects
    """

    from tests.test_app.models import User


    def run(app=None):
        print(User.objects.count())
        print('hello world')




Typical uses would be to
