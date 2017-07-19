from flaskutils.test import FlaskTestCase
from flaskutils.db.exceptions import NotFoundError
from flaskutils.db.postgresql.connection import get_pool

from tests.test_app.models import User
from tests.test_app.serializers import GetUserSerializer, PostUserSerializer
from .models import Artist, Album, Genre  # noqa

from unittest.mock import Mock

import pytest


class TestCaseModel(FlaskTestCase):
    def setup(self):
        super(TestCaseModel, self).setup()
        self.pool = get_pool()

    def test_simple_insert(self):
        assert 0 == Artist.objects.count()
        artist = Artist()
        artist.add()
        self.pool.commit()
        assert 1 == Artist.objects.count()
        artist2 = Artist()
        artist2.add()
        self.pool.commit()
        assert 2 == Artist.objects.count()

    def test_multi_insert(self):
        assert 0 == Genre.objects.count()
        data = [
            Genre(
                name='genre{}'.format(x), description='descript{}'.format(x))
            for x in range(100)
        ]

        Genre.objects.add_all(data)
        self.pool.commit()
        assert 100 == Genre.objects.count()

    def test_relationships(self):
        rock = Genre(name='Rock', description='rock yeah!!!')
        rock.add()
        self.pool.commit()
        pink = Artist(
            genre_id=rock.id, name='Pink Floyd', description='Awsome')
        pink.add()
        self.pool.commit()
        dark = Album(
            artist_id=pink.id, name='Dark side of the moon',
            description='Interesting')
        dark.add()
        self.pool.commit()
        rolling = Artist(
            genre_id=rock.id, name='Rolling Stones', description='Acceptable')

        rolling.add()
        self.pool.commit()

        hits = Album(
            artist_id=rolling.id, name='Greatest hits',
            description='Interesting')
        hits.add()
        self.pool.commit()
        assert 2 == Album.objects.count()

        wall = Album(
            artist_id=pink.id, name='The Wall',
            description='Interesting')
        wall.add()
        self.pool.commit()
        assert 2 == len(pink.albums)
        assert 2 == len(Artist.objects.filter_by(genre_id=rock.id)[:])

    def test_update(self):
        rock = Genre(name='Rock', description='rock yeah!!!')
        rock.add()
        self.pool.commit()
        description_updated = 'description_updated'
        rock.description = description_updated
        rock.update()
        self.pool.commit()
        rock2 = Genre.objects.get(id=rock.id)
        assert rock2.description == description_updated
        assert 1 == Genre.objects.count()

    def test_get_for_update(self):
        rock = Genre(name='Rock', description='rock yeah!!!')
        rock.add()
        self.pool.commit()
        rock2 = Genre.objects.get_for_update(id=rock.id)
        assert rock2.id == rock.id

    def test_delete(self):
        rock = Genre(name='Rock', description='rock yeah!!!')
        rock.add()
        self.pool.commit()
        assert 1 == Genre.objects.count()
        rock.delete()
        self.pool.commit()
        assert 0 == Genre.objects.count()

    def test_raw_sql(self):
        rock = Genre(name='Rock', description='rock yeah!!!')
        rock.add()
        self.pool.commit()
        pink = Artist(
            genre_id=rock.id, name='Pink Floyd', description='Awsome')
        pink.add()
        self.pool.commit()
        dark = Album(
            artist_id=pink.id, name='Dark side of the moon',
            description='Interesting')
        dark.add()
        self.pool.commit()
        rolling = Artist(
            genre_id=rock.id, name='Rolling Stones', description='Acceptable')

        rolling.add()
        self.pool.commit()
        sql = """
            SELECT a.name as artist_name, a.description artist_description,
            g.name as artist_genre
            FROM artist a
            INNER JOIN genre g ON a.genre_id = g.id
            ORDER BY a.id DESC;
        """

        result = Genre.objects.raw_sql(sql).fetchall()
        assert 2 == len(result)
        assert 'Rolling Stones' == result[0][0]

        sql = """
            SELECT a.name as artist_name, a.description artist_description,
            g.name as artist_genre
            FROM artist a
            INNER JOIN genre g ON a.genre_id = g.id
            WHERE a.id = :artist_id
            ORDER BY a.id DESC;
        """

        result = Genre.objects.raw_sql(sql, artist_id=pink.id).fetchall()
        assert 1 == len(result)
        assert 'Pink Floyd' == result[0][0]

    def test_not_found(self):
        with pytest.raises(NotFoundError) as excinfo:
            Genre.objects.get(id=-666)
        assert "Object not found" in str(excinfo.value)

    def test_encrypted_password(self):
        user = User(username='username', email='eil@il.com', password='123')
        user.add()
        self.pool.commit()
        id = user.id
        # objects needs to dereferenciated otherwise
        # user2 will be just a copy of user
        user = None
        user2 = User.objects.get(id=id)
        assert id == user2.id
        assert '123' == user2.password

    def test_model_to_json(self):
        assert 0 == User.objects.count()
        user = User(
            username='username1', email='email1@email.com', password='123')
        user.add()
        self.pool.commit()

        user2 = User.objects.get(id=user.id)
        serializer = GetUserSerializer(model=user2)
        json_model = serializer.to_json()
        assert user2.id == json_model['id']
        assert user2.username == json_model['username']
        assert user2.email == json_model['email']
        assert 'password' not in json_model

    def test_serializer_to_model(self):
        request = Mock()
        user_dict = {
            'username': 'userupdated', 'password': '123',
            'email': 'email@test.com'}
        request.json = user_dict
        data = PostUserSerializer(request=request).to_json()
        user_model = User(**data)
        assert user_dict['username'] == user_model.username
        assert user_model.email == user_dict['email']
