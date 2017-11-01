Flask-Philo Views
==========================

Most of the applications we build with Flask-Philo are simple REST APIs.
You can use Flask-Philo to do more complicated things but the most common thing
we do is return blocks oj JSON from REST endpoints.

We keep most of our appications views in a ``views`` folder in ``src/app``.

They all inherit from ``flask_philo.views.BaseResourceView``.


Here's an example view for a GET endpoint that returns a simple JSON message:

::

 from flask_philo.views import BaseView, BaseResourceView

  class MyView(BaseResourceView):
      methods = ['GET']

      def get(self, *args, **kwargs):
          return self.json_response(200, {'message': 'Here it is'})



The next thing to do is create some tuple values in ``src/app/urls.py`` to specify
the url for the endpoint you want to expose:

E.g.

::

  from app.views import MyView

  URLS = (
	 ('/api/resource/myresource', MyView, 'my view')
  )


Now, when you run the server and make a GET request to ``/api/resource/myresource``,
the application should respond with a status of ``200`` and ``JSON data``.




JSON Serializers
---------------------------------------------------------

A serializer is a mechanism that we use in Flask-Philo to deserialize data in a
safe way. The main principle behind serializers is that data sent by users can
not be trusted by default. To create a serializer you must inherit from 
``flask_philo.serializers.BaseSerializer`` and define the ``_shcema`` property
following the rules specified in `jsonschema <http://json-schema.org/>`_

E.g.

::

    class PostUserSerializer(BaseSerializer):
        _schema = {
            'type': 'object',
            'properties': {
                'email': {'type': 'string', 'format': 'email'},
                'username': {'type': 'string'},
                'last_login': {'type': 'string', 'format': 'date-time'},
                'birthday': {'type': 'string', 'format': 'date'},
                'password': {'type': 'string'},
            },
            'required': ['email', 'username', 'password']
        }



        data = PostUserSerializer(request=request).to_json()
