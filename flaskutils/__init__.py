from flask import Flask
from flask_oauthlib.provider import OAuth2Provider

from . import default_settings
from .commands_flaskutils import *  # noqa
from .exceptions import ConfigurationError

import flask_login
import logging
import importlib
import os


# Alex Martelli's 'Borg'
class Borg:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state

app = None
login_manager = flask_login.LoginManager()
oauth = OAuth2Provider()


def get_login_manager():
    return app.login_manager


def init_app(module, BASE_DIR, testing=True):
    """
    Initalize an app, call this method once from start_app
    """
    global app
    global login_manager

    def init_config():
        """
        Load settings module and attach values to the application
        config dictionary
        """
        if 'FLASKUTILS_SETTINGS_MODULE' not in os.environ:
            raise ConfigurationError('No settings has been defined')

        app.config['BASE_DIR'] = BASE_DIR

        # default settings
        for v in dir(default_settings):
            if not v.startswith('_'):
                app.config[v] = getattr(default_settings, v)

        app.debug = app.config['DEBUG']

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

        def init_flask_login():
            """
            Initialize flask login
            https://flask-login.readthedocs.io
            """
            login_manager.session_protection = 'strong'
            login_manager.init_app(app)

        def init_flask_oauthlib():
            """
            http://flask-oauthlib.readthedocs.io/en/latest/oauth2.html
            """
            oauth.init_app(app)

        init_logging()
        init_urls()
        init_postgres(testing)
        init_flask_login()
        init_flask_oauthlib()

    app = Flask(module)
    init_config()


def execute_command(cmd, **kwargs):
    """
    execute a console command
    """
    cmd_dict = {
        c: 'flaskutils.commands_flaskutils.' + c for c
            in dir(commands_flaskutils) if not c.startswith('_') and c != 'os'  # noqa
    }

    # loading specific app commands
    try:
        import console_commands
        for cm in console_commands.__all__:
            if not cm.startswith('_'):
                cmd_dict[cm] = 'console_commands.' + cm
    except Exception as e:
        print(e)
        pass

    if cmd not in cmd_dict:
        raise ConfigurationError('command {} does not exists'.format(cmd))
    cmd_module = importlib.import_module(cmd_dict[cmd])
    kwargs['app'] = app
    cmd_module.run(**kwargs)
