from flaskutils.models import FlaskModel
from flaskutils.exceptions import AuthenticationError
from flaskutils.sql import BcryptType, Password
from pgsqlutils.exceptions import NotFoundError
from flask_login import UserMixin
from sqlalchemy import Boolean, Column, String


class User(FlaskModel, UserMixin):
    __tablename__ = 'users'
    username = Column(String(64))
    password = Column(BcryptType)
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
            assert Password(user.password) == Password(password)
            return user
        except (AssertionError, NotFoundError,):
            raise AuthenticationError('invalid credentials')
