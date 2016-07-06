from flaskutils.models import FlaskModel
from flaskutils.exceptions import AuthenticationError
from pgsqlutils.types import Password, BcryptType
from pgsqlutils.exceptions import NotFoundError

from sqlalchemy import Boolean, Column, String


class User(FlaskModel):
    __tablename__ = 'users'
    username = Column(String(64))
    password = Column(BcryptType)
    email = Column(String(64))
    is_active =  Column(Boolean(), nullable=False, default=False)

    @classmethod
    def authenticate(cls, username=None, email=None, password=None):

        # checking if all fiels are not null
        if not(username and email and password):
            raise AuthenticationError('invalid credentials')

        try:
            user = User.objects.get(username=username, email=email)
            assert Password(user.password, password.encode('utf-8'))
            return user
        except NotFoundError:
            raise AuthenticationError('invalid credentials')
