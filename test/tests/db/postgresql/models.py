from flaskutils.db.postgresql.orm import BaseModel

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
