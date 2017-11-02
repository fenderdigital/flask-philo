# Flask-Philo

Small and very opinionated framework to build flask based microservices.

You can check the official documentation [here](http://flask-philo.readthedocs.io/en/latest/)


## What this project is about?

Flask is an awesome web microframework that works great out of the box. Nevertheless,
additional configuration and integration with complementary libraries are required 
in order to build complex applications. Here in [riffstation.com](https://play.riffstation.com) we have several
HTTP REST based microservices, anytime that we want to create a new microservice we need to bootstrap
very similar common code.

This framework collect all the logic related with HTTP, REST and data access in one common place.
Feel free to use it and extend it. We are willing to hear about your suggestions and improvements.


## Installation

```
pip3 install Flask-Philo
```


## Executing test

In order to run test a vagrant instance is required, below steps required to execute unit tests:

```
   cd test
   vagrant up
   vagrant ssh
   cd /src/test
   python3 manage.py test
```


## Basic Features

* REST out of the box.

* Simple sqlalchemy orm customized for postgresql with multiple dabatases.

* Simple Redis integration.

* Simple Elastic Search integration.

* Basic AWS integration.


## External Resources

* [Flask Website](http://flask.pocoo.org/)

* [Flask Book](http://flaskbook.com/)

* [SQL Alchemy](http://www.sqlalchemy.org/)

* [Python Redis](https://pypi.python.org/pypi/redis/2.10.3)

* [Python Elastic Search](https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/index.html)

* [AWS Boto](https://pypi.python.org/pypi/boto3)


## Creating a new project
Flask-Philo includes the `flask-philo-admin` command line tool.
To quickly generate a new Flask-Philo project, navigate to the directory in which you want to create
the project and run:

```
flask-philo-admin startproject <project_name>
```

This will create a folder called project_name which will contain the basic structure of a Flask-Philo application,
basic unit tests and configuration.
