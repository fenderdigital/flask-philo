## Using multiple databases

Flaskutils allows you to connect to multiple database instances in the same application. For example, sometimes we need to access a Postgresql database and a Redis cache from the same application.

To take advantage of this feature, simply add a `DATABASES` block in an application config filr in `src/config`.

Here's an example of a config that we use in some applications:
```
DATABASES = {
    'POSTGRESQL': {
        'DEFAULT': "postgresql://dev:password@localhost/db_name",
    },
    'REDIS': {
        'DEFAULT': {
            'HOST': 'localhost',
            'PORT': 6379,
            'DB': 0,
            'PASSWORD': 'password'
        }
    }
}
```
