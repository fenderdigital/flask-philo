from flask import Flask, g
from flask_oauthlib.provider import OAuth2Provider
from . import default_settings
from .commands_flask_philo import *  # noqa
from .jinja2 import init_jinja2
from .exceptions import ConfigurationError
from .db import init_db

import logging
import importlib
import os


# Alex Martelli's 'Borg'
class Borg:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


app = None
oauth = OAuth2Provider()


def init_app(module, BASE_DIR, **kwargs):
    """
    Initalize an app, call this method once from start_app
    """
    global app

    def init_config():
        """
        Load settings module and attach values to the application
        config dictionary
        """
        if 'FLASK_PHILO_SETTINGS_MODULE' not in os.environ:
            raise ConfigurationError('No settings has been defined')

        app.config['BASE_DIR'] = BASE_DIR

        # default settings
        for v in dir(default_settings):
            if not v.startswith('_'):
                app.config[v] = getattr(default_settings, v)

        app.debug = app.config['DEBUG']

        # app settings
        settings = importlib.import_module(
            os.environ['FLASK_PHILO_SETTINGS_MODULE'])
        for v in dir(settings):
            if not v.startswith('_'):
                app.config[v] = getattr(settings, v)

        def init_urls():
            # Reads urls definition from URLs file and bind routes and views
            urls_module = importlib.import_module(app.config['URLS'])
            for route in urls_module.URLS:
                app.add_url_rule(
                    route[0], view_func=route[1].as_view(route[2]))

        def init_logging():
            """
            initialize logger for the app
            """
            hndlr = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') # noqa
            hndlr.setFormatter(formatter)
            app.logger.addHandler(hndlr)
            log_level = app.config['LOG_LEVEL']
            app.logger.setLevel(getattr(logging, log_level))

        def init_flask_oauthlib():
            """
            http://flask-oauthlib.readthedocs.io/en/latest/oauth2.html
            """
            oauth.init_app(app)
        init_db(g, app)
        init_logging()
        init_urls()
        init_flask_oauthlib()
        init_jinja2(g, app)

    app = Flask(module)
    init_config()
    return app


def execute_command(cmd, **kwargs):
    """
    execute a console command
    """
    cmd_dict = {
        c: 'flask_philo.commands_flask_philo.' + c for c
            in dir(commands_flask_philo) if not c.startswith('_') and c != 'os'  # noqa
    }

    # loading specific app commands
    try:
        import console_commands
        for cm in console_commands.__all__:
            if not cm.startswith('_'):
                cmd_dict[cm] = 'console_commands.' + cm
    except Exception:
        pass

    if cmd not in cmd_dict:
        raise ConfigurationError('command {} does not exists'.format(cmd))
    cmd_module = importlib.import_module(cmd_dict[cmd])
    kwargs['app'] = app
    cmd_module.run(**kwargs)
