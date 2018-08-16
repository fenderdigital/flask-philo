SQL Alchemy ORM for Postgresql
=======================================

Flask-Philo uses SQLAlchemy as its Object Relational Mapper (ORM). For mode detail and documentation on SQL Alchemy, visit `<https://www.sqlalchemy.org/>`_


Where is Flask-Philo's PostgreSQL ORM implementation?
-----------------------------------------------

Flask-Philo's PostgreSQL ORM can be found at:

`<https://github.com/Riffstation/flask-philo/tree/dev/flask_philo/db/postgresql>`_


Database Settings
-----------------

The first
thing you need to do is to add the relevant configuration
to your application's settings file, typically ``<your_app>/config/development.py`` :

::

    DATABASES = {
        'POSTGRESQL': {
            'DEFAULT': 'postgresql://user:password@host:port/database_name',
        },
    }



Models
======

In order to create Flask-Philo Models, simply create classes that inherit from Flask-Philo's ``BaseModel`` class:

``flask_philo.db.postgresql.orm.BaseModel``

``BaseModel`` exposes a number of useful methods for retrieving and manipulating data:

* **add()** - create a new Flask-Philo class instance (ORM object)
* **update()** - modify an existing ORM object
* **delete()** - delete an ORM object
* **objects.get(key=value)** - retrieve an ORM object by a specified key
* **objects.filter_by(key=value)** - retrieve a collection of filtered objects by a specified key/keys
* **objects.count()** - count all object instances of a Flask-Philo class
* **objects.raw_sql(sql_query_string)** - run direct SQL queries on your application's database



Example Models
-------------

Here are 3 examples of models with some simple properties and examples of how you can use them in
your application:

::

    from flask_philo.db.postgresql.orm import BaseModel

    from sqlalchemy import Column, ForeignKey, Integer, String
    from sqlalchemy.orm import relationship


    class Artist(BaseModel):
        __tablename__ = 'artist'
        name = Column(String(256))
        description = Column(String(256))
        albums = relationship('Album', backref='artist')
        is_famous = Column(Boolean, default=False)
        genre_id = Column(Integer, ForeignKey('genre.id'))


    class Album(BaseModel):
        __tablename__ = 'album'
        name = Column(String(256))
        description = Column(String(256))
        artist_id = Column(Integer, ForeignKey('artist.id'))


    class Genre(BaseModel):
        __tablename__ = 'genre'
        name = Column(String(256))
        description = Column(String(256))


Flask-Philo's ORM automatically handles the creation of each model's integer ``id`` property, along with automatically creating and updating the timestamp fields ``created_at`` and ``updated_at``

Foreign Keys may be defined using the ``ForeignKey(<key_name>)`` syntax, as is the case in our example **Album** model above. Here, the **Album** model references the **Artist** model (DB table ``artist``) as a foreign key using ``artist.id``


Fields
===========

Field types
-----------

The most common field types are:

- **Column**: defines the properties of a given column

- **relationship**: defines the relationship between two tables


Examples:

::

    class Artist(BaseModel):
        __tablename__ = 'artist'
        name = Column(String(256))
        description = Column(String(256))
        albums = relationship('Album', backref='artist')
        genre_id = Column(Integer, ForeignKey('genre.id'))


Supported data types
-----------

- **String**: stores string format data

::

    name = Column(String(256))


- **Integer**: stores integer format data

::

    amount = Column(Integer)

- **Boolean**: stores boolean format data

::

    is_famous = Column(Boolean, default=False)


- **Numeric**: store numbers with a very large number of digits. Scale is the count of decimal digits in the fractional part. Precision refers to the total count of digits in the whole number.

::

    tempo = Column(Numeric(precision=32, scale=16))


- **ARRAY**: store array data

::

    possible_names = Column(ARRAY(String(256)))


- **JSON**: stores JSON format data

::

    config_dict = Column(JSON)



- **Enum**: provides a set of possible string values that work as constraints for the given column.

::

    day = Column(
        Enum(
            'sunday', 'monday', 'tuesday', 'wednesday', 'thursdat', 'fruday',
            'saturday', name="days_of_the_week"))


Field options
-----------

The following ORM constraints can be set in your Flask-Philo Model:

- **PrimaryKey**: specifies that a given column is a primary key. As such, it is unique and not nullable.

::

    id = Column(Integer, primary_key=True)


- **ForeignKey**: specifies a column that acts as foreign key, thereby defining a relationship with another table

::

    genre_id = Column(Integer, ForeignKey('genre.id'))


- **unique**: specifies that a column must have a unique value for each record

::

    name = Column(String(256), unique=True)


- **nullable**: specifies if a column accepts null values or not

::

    name = Column(String(256), nullable=False, unique=True)


- **default**: defines a default value in the case that it is not specified

::

    is_famous = Column(Boolean, default=False)

----

Database DML Operations
=======================

Postgresql Connection Pool
------------------------------

As a design decision, management of the PostgreSQL connection is the responsability of the developer, but this is made simple with Flask-Philo's built-in connection management methods.

* to instantiate a DB session, we use Flask-Philo's ``get_pool()`` method
* after modifying, creating or removing data in a session, we must commit or rollback the session using Flask-Philo's ``pool.commit()`` or ``pool.rollback()`` methods

Opening a Flask-Philo DB session
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    from flask_philo.db.postgresql.connection import get_pool
    pool = get_pool()
    # Do some ORM operations here
    pool.commit()


The following examples demonstrate each of the core ORM operations you will commonly use to query the PostgreSQL database


Data Manipulation Examples
------------------


Adding a record
^^^^^^^^^^^^^^^

Here you will insert a new genre based on the model (Genre) above:

::

    rock = Genre(name='Rock', description='Rock and Roll')
    rock.add()


Now you have two options: commit or rollback the insert operation.

To commit the operation and create a new record:

::

    pool.commit()


In case the record is not needed, you can rollback the transaction and nothing will be changed in the database:

::

    pool.rollback()


Let's suppose you've created and committed the new genre.

Now you can retrieve the record from the database by using the filter_by function:

::

    rock = Genre.objects.filter_by(name="Rock").first()


You can retrieve column values for the record above:

::

    print(rock.name)


It will print:

::

    Rock


Updating a record
^^^^^^^^^^^^^^^

The same way you retrieve a record, you can update it. Here follows an example:

::

    rock = Genre.objects.filter_by(name="Rock").first()
    rock.name = "Metal"
    rock.update()
    pool.commit()

    metal = Genre.objects.filter_by(name="Metal").first()

    # Will print "Metal"
    print(metal.name)


Deleting a record
^^^^^^^^^^^^^^^

In the same way you've added and updated a record, we can delete it:

::

    metal = Genre.objects.filter_by(name="Metal").first()
    metal.delete()
    pool.commit()


This way the record should no longer exist.


Querying using Raw SQL
^^^^^^^^^^^^^^^

You can use the ``raw_sql`` command to run queries also, like the following example:

::

    raw_sql_genre = Genre.objects.raw_sql("SELECT description FROM genre WHERE name='Jazz';").fetchone()
    genre_description = raw_sql_genre.description


Another example using raw sql:

::

    count = Genre.objects.raw_sql("SELECT count(*) FROM genre;").fetchone()[0]


The variable ``count`` will return the number of lines in genre table.

An easy way to count records in a table is to use the following syntax:

::

    count = Genre.objects.count()


Examples using relations
------------------------

::

        dark = Album(
            artist_id=pink.id, name='Dark side of the moon',
            description='Interesting')
        dark.add()
        pool.commit()
        rolling = Artist(
            genre_id=rock.id, name='Rolling Stones',
            description='Acceptable')

        rolling.add()
        pool.commit()

        hits = Album(
            artist_id=rolling.id, name='Greatest hits',
            description='Interesting')
        hits.add()
        pool.commit()
        assert 2 == Album.objects.count()

        wall = Album(
            artist_id=pink.id, name='The Wall',
            description='Interesting')
        wall.add()
        pool.commit()



Using multiple Postgresql databases
-------------------------------------

Flask-Philo allows you to connect to multiple postgresql database instances in the same
application.

To take advantage of this feature, simply add a ``DATABASES`` block in an application
configuration file in ``src/config``.

Here's an example of a configuration  that we use in some applications:

::

 DATABASES = {
     'POSTGRESQL': {
         'DEFAULT': 'postgresql://user:password@host:port/database_name',
         'MUSIC_CATALOG': 'postgresql://user:password@host:port/songs_database_name',
     }
 }


Now you can access to the specific database using ``flask_philo.db.postgresql.connection.get_pool``:

::

        blues = Genre(name='Blues', description='Still got the blues')
        blues.add()
        pool.commit(connection_name='MUSIC_CATALOG'))
