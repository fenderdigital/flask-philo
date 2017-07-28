# flaskutils

Utils to build flask based microservices.

## What this project is about?

Flask is an awsome web microframework that works great out of the box. Nevertheless,
additional configuration and integration with complementaries libraries are required 
in order to build complex applications. Here in riffstation.com we have several HTTP REST
based microservices, anytime that we want to create a new microservice we need to bootstrap
very similar common code.

This library wants to concentrate all logic related with HTTP and REST in one common place.
Feel free to use it and extendent it. We are willing to hear about your suggestions and improvements.

## Executing test

In order to run test a vagrant instance is required, below steps required to execute unit tests:

```
   cd test
   vagrant up
   vagrant ssh
   cd /src/test
   python3 manage.py test
```



## External Resources

* [Flask Website](http://flask.pocoo.org/)

* [Flask Book](http://flaskbook.com/)


## Creating a new project
Flaskutils includes the `flaskutils-admin` command line tool.
To quickly generate a new flaskutils project, navigate to the directory in which you want to create the project and run:

```
flaskutils-admin startproject <project_name>
```

This will create a folder called project_name which will contain the basic structure of a flaskutils application, including a Vagrantfile, basic unit tests and bdd tests and configuration.
