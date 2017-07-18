from flaskutils.db.postgresql.orm import BaseModel
from flaskutils.exceptions import AuthenticationError
from flaskutils.db.postgresql.types import Password
from flaskutils.db.exceptions import NotFoundError
from flask_login import UserMixin
from sqlalchemy import Boolean, Column, String


class User(BaseModel, UserMixin):
    __tablename__ = 'users'
    username = Column(String(64))
    password = Column(Password)
    email = Column(String(64))
    is_active = Column(Boolean(), nullable=False, default=False)

    def get_id(self):
        return self.id

    @classmethod
    def authenticate(cls, username=None, email=None, password=None):
        # checking if all fiels are not null
        if not(username and email and password):
            raise AuthenticationError('invalid credentials')

        try:
            user = User.objects.get(username=username, email=email)
            assert user.password == password
            return user
        except (AssertionError, NotFoundError,):
            raise AuthenticationError('invalid credentials')
