SQL Alchemy ORM for Postgresql
=======================================

Flask-Philo uses SQLAlchemy as an ORM.


Where's Postgresql ORM on Flask-Philo project
-----------------------------------------------

Flask-Philo Postgresql ORM can be found at:


https://github.com/Riffstation/flask-philo/tree/dev/flask_philo/db/postgresql


The first
thing you need to do is to add the relevant configuration
to your settings file:

::


    DATABASES = {
        'POSTGRESQL': {
            'DEFAULT': 'postgresql://user:password@host:port/database_name',
        },
    }



Creating Database Models
----------------------------

In order to create simple models all you have to do is
create classes that inherit from Flask-Philo ``flask_philo.db.postgresql.orm.BaseModel``.


``BaseModel`` exposes a number of methods for retrieving and manipulating data.

Here's 3 examples of models with some simple properties and examples of how you can use them in
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



Postgresql Connection Pool
------------------------------

One of the design decisions taken for the development team was to leave to the
developer the management of the Postgresql connection, therefore, it is developers
responsablity to commit or rollback the  `SQL Alchemy <http://www.sqlalchemy.org/>`_
session using ``flaskutils.db.postgresql.connection.get_pool``

::

      from flaskutils.db.postgresql.connection import get_pool
      pool = get_pool()


The following are examples are about how to use the ORM to query the database:

::

        rock = Genre(name='Rock', description='rock yeah!!!')
        rock.add()
        pool.commit()
        pink = Artist(
            genre_id=rock.id, name='Pink Floyd', description='Awsome')
        pink.add()
        pool.commit()
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
        assert 2 == len(pink.albums)
        assert 2 == len(Artist.objects.filter_by(genre_id=rock.id)[:])



Using multiple Postgresql databases
-------------------------------------

Flask-Philo allows you to connect to multiple postgresql database instances in the same
application. 

To take advantage of this feature, simply add a `DATABASES` block in an application
configuration file in `src/config`.

Here's an example of a configuration  that we use in some applications:

::

 DATABASES = {
     'POSTGRESQL': {
         'DEFAULT': 'postgresql://user:password@host:port/database_name',
         'MUSIC_CATALOG': 'postgresql://user:password@host:port/songs_database_name',
     }
 }


Now you can access to the specific database using ``flaskutils.db.postgresql.connection.get_pool``:

::

        rock = Genre(name='Rock', description='rock yeah!!!')
        rock.add()
        pool.commit(connection_name='MUSIC_CATALOG'))
