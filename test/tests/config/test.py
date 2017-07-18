from .development import *  # noqa


USERNAME = 'username'

PASSWORD = 'password'


DATABASES = {
    'POSTGRESQL': {
        'DEFAULT': 'postgresql://ds:dsps@localhost:5432/ds_test',
        'DB2': 'postgresql://ds:dsps@localhost:5432/ds2_test'
    }
}
