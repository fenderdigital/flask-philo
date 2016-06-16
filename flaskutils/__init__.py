from flask import Flask

from .exceptions import  ConfigurationError

import importlib
import os


# Alex Martelli's 'Borg'
class Borg:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class App(Borg):
    """
    Singleton class that shares app properties accross
    all components in the application
    """
    def __init__(self, module, **config):
        Borg.__init__(self)
        self.flask_app = Flask(module)
        self.init_config()

    def init_config(self, **config):

        for k, v in config.items():
            self.app.config[k] = v

        if 'SECRET_KEY' in config:
            app.secret_key = config['SECRET_KEY']




    def init_urls(self):
        # Reads urls definition from URLs file and bind routes and views
        if 'URLS' in self.flask_app.config:
            for route in self.flask_app.config['URLS']:
                self.flask_app.add_url_rule(
                    route[0], view_func=route[1].as_view(route[2]))


app = None


def init_app(module):
    """
    Initalize an app, call this method once from start_app
    """
    global app

    def init_config():
        if 'FLASKUTILS_SETTINGS_MODULE' not in os.environ:
            raise ConfigurationError('No settings has been defined')

        settings = importlib.import_module(os.environ['FLASKUTILS_SETTINGS_MODULE'])
        for v in dir(settings):
            if not v.startswith('_'):
                app.config[v] = getattr(settings, v)
        import ipdb; ipdb.set_trace()

    app = Flask(module)
    init_config()
