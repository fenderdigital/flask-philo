from flask_philo.db.postgresql.orm import BaseModel
from flask_philo.exceptions import AuthenticationError
from flask_philo.db.postgresql.types import Password
from flask_philo.db.exceptions import NotFoundError
from sqlalchemy import Boolean, Column, String, Numeric


class User(BaseModel):
    __tablename__ = 'users'
    username = Column(String(64))
    password = Column(Password)
    email = Column(String(64))
    is_active = Column(Boolean(), nullable=False, default=False)
    credit_score = Column(Numeric(), nullable=True)

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
