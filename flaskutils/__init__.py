from flask import Flask

from .exceptions import  ConfigurationError

import importlib
import os


# Alex Martelli's 'Borg'
class Borg:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state

app = None


def init_app(module):
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

        settings = importlib.import_module(os.environ['FLASKUTILS_SETTINGS_MODULE'])
        for v in dir(settings):
            if not v.startswith('_'):
                app.config[v] = getattr(settings, v)

        def init_urls():
            # Reads urls definition from URLs file and bind routes and views
            urls_module = importlib.import_module(app.config['URLS'])
            for route in urls_module.URLS:
                app.add_url_rule(
                        route[0], view_func=route[1].as_view(route[2]))
        init_urls()

    app = Flask(module)
    init_config()
