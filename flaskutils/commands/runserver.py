from flaskutils.exceptions import ConfigurationError


def run(app, **kwargs):
    if app.config['DEBUG']:
        app.run(
            host=app.config['HOST'], port=app.config['PORT'])
    else:
        raise ConfigurationError(
            'Development server can run just in DEBUG mode')
