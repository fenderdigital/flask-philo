from flask_philo.exceptions import ConfigurationError


def run(**kwargs):
    app = kwargs['app']
    if app.config['DEBUG']:
        app.run(
            host=app.config['HOST'], port=app.config['PORT'])
    else:
        raise ConfigurationError(
            'Development server only can run in DEBUG mode')
