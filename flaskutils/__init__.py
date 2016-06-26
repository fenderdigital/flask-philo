from flask import Flask

from . import default_settings
from .exceptions import ConfigurationError

import logging
import importlib
import os


# Alex Martelli's 'Borg'
class Borg:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state

app = None


def init_app(module, testing=True):
    """
    Initalize an app, call this method once from start_app
    """
    global app

    def init_config():
        """
        Load settings module and attach values to the application
        config dictionary
        """
        if 'FLASKUTILS_SETTINGS_MODULE' not in os.environ:
            raise ConfigurationError('No settings has been defined')

        # default settings
        for v in dir(default_settings):
            if not v.startswith('_'):
                app.config[v] = getattr(default_settings, v)

        # app settings
        settings = importlib.import_module(
            os.environ['FLASKUTILS_SETTINGS_MODULE'])
        for v in dir(settings):
            if not v.startswith('_'):
                app.config[v] = getattr(settings, v)

        def init_urls():
            # Reads urls definition from URLs file and bind routes and views
            urls_module = importlib.import_module(app.config['URLS'])
            for route in urls_module.URLS:
                app.add_url_rule(
                        route[0], view_func=route[1].as_view(route[2]))

        def init_postgres(testing):
            """
            If postgresql url is defined in configuration params a
            scoped session will be created and will be used by
            pgsqlutils
            https://github.com/Riffstation/sqlalchemypostgresutils
            """
            if 'POSTGRESQL_DATABASE_URI' in app.config:
                if not testing:
                    # not testing will use request context as scope
                    # for sqlalchemy Session object
                    from flask import _app_ctx_stack
                    import pgsqlutils.base as pgbase
                    from pgsqlutils.base import get_db_conf, init_db_conn
                    from sqlalchemy.orm import sessionmaker, scoped_session
                    dbconf = get_db_conf()
                    dbconf.DATABASE_URI = app.config['POSTGRESQL_DATABASE_URI']
                    # monkey patching to replace default session
                    # by a sessing handled by flask
                    pgbase.Session = scoped_session(
                        sessionmaker(),
                        scopefunc=_app_ctx_stack.__ident_func__)
                    init_db_conn()
                else:
                    # Testing will use current thread as scope for Session
                    from pgsqlutils.base import get_db_conf, init_db_conn
                    dbconf = get_db_conf()
                    dbconf.DATABASE_URI = app.config['POSTGRESQL_DATABASE_URI']
                    init_db_conn()

        def init_logging():
            """
            initialize logger for the app
            """
            app.logger.addHandler(logging.StreamHandler())
            log_level = app.config['LOG_LEVEL']
            app.logger.setLevel(getattr(logging, log_level))

        init_urls()
        init_postgres(testing)
        init_logging()

    app = Flask(module)
    init_config()
