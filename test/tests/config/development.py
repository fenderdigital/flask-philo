URLS = 'tests.test_app.urls'

DATABASES = {
    'POSTGRESQL': {
        'DEFAULT': 'postgresql://ds:dsps@localhost:5432/ds',
        'DB2': 'postgresql://ds:dsps@localhost:5432/ds2'
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


DEBUG = True

CRYP_SALT = b'$2b$08$CfrxMjR3SlGKt/6oz3o15.'


SECRET_KEY = 's3cr3t'
