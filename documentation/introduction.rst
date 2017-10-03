Flaskutils
==========

Utilities to build flask based microservices.

What this project is about?
---------------------------

Flask is an awesome web microframework that works great out of the box. Nevertheless, additional configuration and integration with complimentary libraries is required in order to build complex applications. Here at Riffstation we have several HTTP REST-based microservices and whenever we want to create a new microservice we need to bootstrap very similar common code.

This library wants to concentrate all logic related with HTTP and REST in one common place.
Feel free to use it and extend it. We are willing to hear about your suggestions and improvements.

Executing test
--------------

In order to run tests, a vagrant instance is required. Follow the steps below to execute unit tests:

::

   cd testdirectory
   vagrant up
   vagrant ssh
   cd /src/testdirectory
   python3 manage.py test


Basic Features
--------------

- REST out of the box.
- Simple sqlalchemy orm customized for postgresql with multiple dabatases.


External Resources
------------------

- `Flask Website<http://flask.pocoo.org/>`_
- `Flask Book<http://flaskbook.com/>`_
