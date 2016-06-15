# flaskutils

Utils to build flask based microservices.

## What this project is about?

Flask is an awsome web microframework that works great out of the box. Nevertheless, additional configuration
and integration with complementaries libraries are required  in order to build complex applications.
Here in riffstation.com we have several HTTP REST based microservices, anytime that we want to create a
new microservice we need to bootstrap very similar common code.

This library wants to concentrate all logic related with HTTP and REST in one common place.
Feel free to use it and extendent it. We are willing to hear about your suggestions and improvements.

## Executing test

In order to run test a vagrant instance is required, below steps required to execute unit tests:

```
   cd test
   vagrant up
   vagrant ssh
   cd /src/test
   python3 run_test.py
```



## External Resources

* [Flask Website](http://flask.pocoo.org/)

* [Flask Book](http://flaskbook.com/)

* [Flasky](https://github.com/miguelgrinberg/flasky)

* [Flask Restful](http://flask-restful-cn.readthedocs.io/en/0.3.4/)
