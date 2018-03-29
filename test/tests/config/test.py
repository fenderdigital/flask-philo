from .development import *  # noqa

import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


USERNAME = 'username'

PASSWORD = 'password'


JINJA2_TEMPLATES = {
    'DEFAULT': {
        'LOADER': 'FileSystemLoader',
        'PARAMETERS': {
            'path': (
                os.path.join(BASE_DIR, '../', '_templates'),
            ),
            'encoding': 'utf-8',
            'followlinks': False
        },
        'AUTOESCAPING': {
            'enabled_extensions': ('html', 'htm', 'xml'),
            'disabled_extensions': [],
            'default_for_string': True,
            'default': False
        },
        'EXTENSIONS': (
            'tests.test_app.templatetags.TestExtension',
        )
    }
}


DATABASES = {
    'POSTGRESQL': {
        'DEFAULT': 'postgresql://ds:dsps@localhost:5432/ds_test',
        'DB2': 'postgresql://ds:dsps@localhost:5432/ds2_test'
    },

    'REDIS': {
        'DEFAULT': {
            'HOST': 'localhost',
            'PORT': 6379,
            'DB': 0
        }
    },

    'ELASTICSEARCH': {
        'DEFAULT': {
            'HOSTS': [
                {'host': 'localhost', 'port': '9200'}
            ]
        }
    }
}
