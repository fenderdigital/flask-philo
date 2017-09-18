### Views

Most of the applications we build with Flaskutils are simple REST APIs. You can use Flaskutils to do more complicated things but the most common thing we do is return blocks oj JSON from REST endpoints.

We keep most of our appications views in a `views` folder in `src/app`. They all inherit from Flaskutils `BaseResourceView`.

Here's an example view for a GET endpoint that returns a simple JSON message:

```
class MyView(BaseResourceView):
	methods = ['GET']

	def get(self, *args, **kwargs):
		return self.json_response(200, {'message': 'Here it is'})
```

The next thing to do is create some tuple values in `src/app/urls.py` to specify the url for the endoint you want to expose:

E.g.
```
from app.views import MyView

URLS = {
	('/api/resource/myresource', MyView, 'my view')
}
```

Now, when you run the server and make a GET request to /api/resource/myresource, the application should respond with a status of 200 and JSON data.
