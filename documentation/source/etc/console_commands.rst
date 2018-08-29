Console Commands
=============================================

Flask-Philo provides a number of console commands to manage core app services and common tasks (e.g. ``runserver``, ``syncdb``, ``test``, etc).

However, Flask-Philo also allows us to *extend* this set of console commands with our own *custom* commands.
This let us write custom utilities and tools that take advantage of the inherent features of a Flask-Philo application: Object Relational Mapping, app Views, app Models, DB config, safe DB sessions, etc)

Running Console Commands
--------------------

In general, we use the ``manage.py`` program as our starting point for launching console commands. Many useful commands are already included as part of Flask-Philo:

::

    $ python3 manage.py runserver
    $ python3 manage.py test
    $ python3 manage.py syncdb


Writing Custom Console Commands
--------------------

We can extend our application's set of utility commands by adding Python programs to the ``src/console_commands`` directory. For example, when we save the following code to ``src/console_commands/count_users.py``, we now have a simple console command that counts our application's Users, and outputs it to the console:

``src/console_commands/count_users.py``
::

    #!/usr/bin/env python
    """
    Example console command that outputs a count of all User objects
    """

    from tests.test_app.models import User  # Import our 'User' ORM definition

    def run(app=None):
        user_count = User.objects.count()   # Use 'count()' ORM function
        print('User count :', user_count)


Once this simple program is saved to the ``src/console_commands`` directory, it can be run as follows:

::

    $ python3 manage.py count_users
    User count : 13


From this very simple example, we can see how our console command benefits from Flask-Philo's convenient ORM representation of our application's ``Users`` object, and its inherited class functions.
Typical uses for custom console commands could include exporting data dumps/reports, safe import/modification of data, sample data population/initialisation, etc.


Arguments to Console Commands
--------------------

Flask-Philo console commands support the use of arguments using double-dashed (``--arg_name``) argument names. For example, the following console command program accepts a ``User.id`` value, and prints that user's details:

``src/console_commands/get_user_data.py``
::

    #!/usr/bin/env python
    """
    Example console command that outputs details for a specified User object
    """

    import argparse
    from tests.test_app.models import User

    def run(**kwargs):

        # Define parsable argument name 'user_id', and ensure that it is a required argument
        parser = argparse.ArgumentParser()
        requiredNamed = parser.add_argument_group('required named arguments')
        requiredNamed.add_argument('--user_id', help='User ID', required=True)

        # Parse arguments
        args, extra_params = parser.parse_known_args()

        # Attempt to retrieve a User object by ID
        user_obj = User.objects.get(id=args.user_id)

        # Output details if match is found
        if user_obj:
            print('User name :', user_obj.name)
            print('User email address :', user_obj.email)
        else:
            print('No user_id match :', args.user_id)


This example console command can be run as follows:

::

    $ python3 manage.py get_user_data --user_id 13
    User name : John Doe
    User email  address : whatsinthebox@seven.com
