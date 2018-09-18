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

...examples for each of these methods are included in the **Data Manipulation Examples** section below


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
        name = Column(String(256), nullable=False)
        description = Column(String(256))
        albums = relationship('Album', backref='artist')
        is_famous = Column(Boolean, default=False)
        genre_id = Column(Integer, ForeignKey('genre.id'))


    class Album(BaseModel):
        __tablename__ = 'album'
        name = Column(String(256), nullable=False)
        description = Column(String(256))
        artist_id = Column(Integer, ForeignKey('artist.id'))


    class Genre(BaseModel):
        __tablename__ = 'genre'
        name = Column(String(256), nullable=False)
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

Adding a new record
^^^^^^^^^^^^^^^

In this example, we create a new **Genre** using the same model defined in the **Example Models** section:

::

    pool = get_pool()
    rock = Genre(name='Rock', description='Rock and Roll')
    rock.add()


At this point, we have added a new instance of the **Genre** model to our DB session, but we still need to either ``commit()`` or ``rollback()`` the insert operation

To commit the operation and create a new record:

::

    pool.commit()


...alternatively, if the record is not needed the transaction can be rolled-back, and nothing will be changed in the PostgreSQL database:

::

    pool.rollback()



Retrieving a specific record
^^^^^^^^^^^^^^^^^^

Now that we've created and committed our new 'Rock' genre, we can retrieve the record directly from the database by using the ``objects.get()`` function:

::

    genre_obj = Genre.objects.get(name="Rock")
    genre_name = genre_obj.name
    genre_id = genre_obj.id
    print("Genre", genre_id, ":", genre_name)   # Will print "Genre 13 : Rock"

...we can also retrieve a record that matches *multiple* field values:

::

    genre_obj = Genre.objects.get(id=13, name="Rock")
    print("Genre", genre_obj.id, ":", genre_obj.name)   # Will print "Genre 13 : Rock"



Filtering records
^^^^^^^^^^^^^^^^^^^^

We may also use Flask-Philo's ``filter_by()`` function to filter records and retrieve a collection of all matching instances of the desired model.

Continuing our **Genre** example from earlier sub-sections:

::

    genre_collection = Genre.objects.filter_by(name="Rock")
    genre_obj = genre_collection.first()
    print("Genre", genre_obj.id, ":", genre_obj.name)   # Will print "Genre 13 : Rock"


Updating a record
^^^^^^^^^^^^^^^

Just as we can retrieve a record, we can update records in a similar manner:

::

    genre_obj = Genre.objects.filter_by(name="Rock").first()
    genre_obj.name = "Metal"
    genre_obj.update()
    pool.commit()

    updated_genre_obj = Genre.objects.filter_by(name="Metal").first()
    print("Genre", updated_genre_obj.id, ":", updated_genre_obj.name)   # Will print "Genre 13 : Metal"


Deleting a record
^^^^^^^^^^^^^^^

In the same way we've added and updated a record, we can also delete it:

::

    genre_obj = Genre.objects.filter_by(name="Metal").first()
    genre_obj.delete()
    pool.commit()

    genre_obj = Genre.objects.filter_by(name="Metal").first()   # genre_obj == None

..once we have committed the ``delete()`` operation, this record no longer exists in our PostgreSQL DB.


Counting records
^^^^^^^^^^^^^^^^

To count the number of instances of a given Model, we can use the ``objects.count()`` method.

::

    genre_count = Genre.objects.count()
    print(genre_count, "Genres present")  # Will print "13 Genres present"


Querying using Raw SQL
^^^^^^^^^^^^^^^

While the use of SQLAlchemy ORM will automatically translate Flask-Philo method
calls to their corresponding PostgreSQL queries, we also provide a means of
directly querying our underlying PostgreSQL database with a raw SQL query.

By passing a valid SQL query-string to the ``objects.raw_sql()`` method, we can
retrieve or update data explicitly, as is the case in the following examples:

Retrieving data by raw SQL:
::

    raw_sql_genre_result = Genre.objects.raw_sql("SELECT description FROM genre WHERE name='Rock';").fetchone()
    genre_description = raw_sql_genre_result.description
    genre_name = raw_sql_genre_result.name
    print(genre_name, "genre description :", genre_description) # Will print "Rock genres description : Rock and Roll"


Modifying data by raw SQL:

::

    query_string = "UPDATE genre SET name='Indie' WHERE id = 13"
    Genre.objects.raw_sql(query_string)




Data manipulation with Relationships
^^^^^^^^^^^^^^^^^^^^^^^

The following example demonstrates the creation and retrieval of objects for two
related models, **Album** and **Artist**, as defined in the *Example Models* section above

::

        # Create and commit an artist record
        floyd_artist_obj = Artist(name='Pink Floyd')
        floyd_artist_obj.commit()
        pink_floyd_id = floyd_artist_obj.id
        pool.commit()

        # Create and commit a related album
        dark_album_obj = Album(
            artist_id=pink_floyd_id, name='Dark side of the moon')
        dark_album_obj.add()
        pool.commit()

        # Create and commit another related album by the same artist
        wall = Album(
            artist_id=pink_floyd_id, name='The Wall',
            description='Interesting')
        wall.add()
        pool.commit()

        # Retrieve all albums by Pink Floyd
        album_results = Album.objects.filter_by(artist_id=pink_floyd_id)
        for album_obj in album_results:
            print("Pink Floyd album :", album_obj.name)

        # Will print:
        # Pink Floyd album : Dark side of the moon
        # Pink Floyd album : The Wall


Using multiple Postgresql databases
-------------------------------------

Flask-Philo allows you to connect to multiple PostgreSQL database instances from the same
application.

To take advantage of this feature, simply add a ``DATABASES`` block in an application
configuration file in ``src/config``.

Here's an example of a typical configuration file:

::

 DATABASES = {
     'POSTGRESQL': {
         'DEFAULT': 'postgresql://user:password@host:port/database_name',
         'MUSIC_CATALOG': 'postgresql://user:password@host:port/songs_database_name',
     }
 }


...with this configuration in place, we can now access a specific database while using Flask-Philo's ``get_pool()`` method:

::

    from flask_philo.db.postgresql.connection import get_pool
    pool = get_pool()

    # Add a Genre object to our session
    blues_obj = Genre(name='Blues', description='Still got the blues')
    blues_obj.add(connection_name='MUSIC_CATALOG')

    # Commit changes to the MUSIC_CATALOG database
    pool.commit(connection_name='MUSIC_CATALOG'))


The ``connection_name==DB_NAME`` parameter may be specified for all other common ORM methods in Flask-Philo
