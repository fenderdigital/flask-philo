from flaskutils import app

from pgsqlutils.types import Password as ParentPassword
from pgsqlutils.types import BcryptType as ParentBcryptType


class Password(ParentPassword):
    def __new__(cls, value, salt=app.config['CRYP_SALT'], crypt=True):
        return ParentPassword.__new__(
            ParentPassword, value, salt=salt, crypt=crypt)


class BcryptType(ParentBcryptType):
    """Coerce strings to bcrypted Password objects for the database.
    """
    def process_bind_param(self, value, dialect):
        return Password(value)

    def process_result_value(self, value, dialect):
        # already crypted, so don't crypt again
        return Password(value, value, False)
