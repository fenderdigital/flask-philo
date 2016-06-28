from flaskutils.models import FlaskModel
from pgsqlutils.types import BcryptType

from sqlalchemy import Column, String


class User(FlaskModel):
    __tablename__ = 'users'
    username = Column(String(64))
    password = Column(BcryptType)
    email = Column(String(64))
