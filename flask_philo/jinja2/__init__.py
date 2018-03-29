from jinja2 import (
    FileSystemLoader, Environment, select_autoescape)

from pydoc import locate


class TemplatesManager:
    """
    Flask-philo may support multiple template loaders
    """
    _shared_state = {}

    environments = {}

    def __init__(self):
        self.__dict__ = self._shared_state

    def set_request(self, r):
        """
        Appends request object to the globals dict
        """
        for k in self.environments.keys():
            self.environments[k].globals['REQUEST'] = r

    def render(self, template_name, engine_name='DEFAULT', **data):
        t = self.environments[engine_name].get_template(template_name)
        return t.render(**data)


templates_manager = TemplatesManager()


def get_manager():
    return templates_manager


DEFAULT_AUTOSCAPING = {
    'enabled_extentions': ('html', 'htm', 'xml'),
    'disabled_extentions': [],
    'default_for_string': True,
    'default': False
}


def get_autoescaping_params(**config):
    if 'AUTOESCAPING' in config:
        autoescaping_params = config['AUTOESCAPING']
    else:
        autoescaping_params = DEFAULT_AUTOSCAPING
    return autoescaping_params


def load_extensions_from_config(**config):
    """
    Loads extensions
    """
    extensions = []
    if 'EXTENSIONS' in config:
        for ext in config['EXTENSIONS']:
            try:
                extensions.append(locate(ext))
            except Exception as e:
                print(e)
    return extensions


def init_filesystem_loader(**config):
    params = {}
    template_location = config['PARAMETERS']['path']
    params['encoding'] = config['PARAMETERS'].get('encoding', 'utf-8')
    params['followlinks'] = config['PARAMETERS'].get('followlinks', False)
    env = Environment(
        loader=FileSystemLoader(template_location, **params),
        autoescape=select_autoescape(**get_autoescaping_params(**config)),
        extensions=load_extensions_from_config(**config)
    )
    return env


def init_loader(app, **config):
    loaders_dict = {
        'FileSystemLoader': init_filesystem_loader
    }
    env = loaders_dict[config['LOADER']](**config)
    env.globals['FLASK_PHILO_CONFIG'] = app.config
    return env


def init_jinja2(g, app):
    if 'JINJA2_TEMPLATES' in app.config:
        for cname, template_config in app.config['JINJA2_TEMPLATES'].items():
            templates_manager.environments[cname] =\
                init_loader(app, **template_config)

        @app.before_request
        def before_request():
            """
            Assign template manager to the global
            flask object at the beginning of every request
            """
            for cname, template_config in\
                    app.config['JINJA2_TEMPLATES'].items():
                env = init_loader(app, **template_config)
                templates_manager.environments[cname] = env
            g.jinja2_template_manager = templates_manager
