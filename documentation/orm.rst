ORM
===

Flaskutils uses SQLAlchemy as an ORM. In our applications, we create simple models that inherit from Flaskutils ``BaseModel``.

BaseModel exposes a number of methods for retrieving and manipulating data.

Here's an example Guitar model with some simple properties and examples of how you can use them in your application:

::

 class Guitar(BaseModel):
	 name = Column(String(256), nullable=False)
	 no_of_strings = Column(Integer)

 Guitar.objects.get(name='name')
	 returns a single result object

 Guitar.objects.filter_by(name='name')
	 returns a list of objects matching the query params

 Guitar.objects.count()
	 returns a count of all the guitars in the DB

 obj = Guitar.objects.get(name='name')
 obj.update()

 obj = Guitar.objects.get(name='name')
 obj.delete()
