from pgsqlutils.orm import BaseModel
from pgsqlutils.types import BcryptType

from sqlalchemy import Column, ForeignKey, Integer, String


class User(BaseModel):
    __tablename__ = 'users'
    username = Column(String(64))
    password = Column(BcryptType)
    email = Column(String(64))
