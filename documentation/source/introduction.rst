Flask-Philo
=============

Utilities to build flask based microservices.




What this project is about?
---------------------------

Flask is an awesome web microframework that works great out of the box. Nevertheless,
additional configuration and integration with complimentary libraries is required in
order to build complex applications. Here at `Riffstation <https://play.riffstation.com/>`_
we have several HTTP REST-based microservices and whenever we want to create a new
microservice we need to bootstrap very similar common code.

This library wants to concentrate all logic related with HTTP, REST, databases in one common place.
Feel free to use it and extend it. We are willing to hear about your suggestions and improvements.


Basic Features
--------------

- REST out of the box.

- Simple sqlalchemy orm customized for postgresql with multiple dabatases.

- Simple Redis integration.

- Simple Elastic Search integration.

- Basic AWS integration.




Creating a new project
----------------------------

Flask-Philo includes the ``flask-philo-admin`` command line tool.

To quickly generate a new Flask-Philo project, navigate to the directory in which you want to create the project and run:

::

 flask-philo-admin startproject <project_name>


This will create a folder called project_name which will contain the basic structure of a Flask-Philo application.



External Resources
------------------

- `Flask Website <http://flask.pocoo.org/>`_

- `Flask Book <http://flaskbook.com/>`_

- `SQL Alchemy <http://www.sqlalchemy.org/>`_

* `Python Redis <https://pypi.python.org/pypi/redis/2.10.3>`_

* `Python Elastic Search <https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/index.html>`_

* `AWS Boto <https://pypi.python.org/pypi/boto3>`_
