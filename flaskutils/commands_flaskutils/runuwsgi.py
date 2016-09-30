from flaskutils.exceptions import ConfigurationError


def run(**kwargs):
    app = kwargs['app']
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        use_reloader=app.config['USE_RELOADER'],
        debug=app.config["DEBUG"]
    )
