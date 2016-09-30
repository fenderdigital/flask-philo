
def run(**kwargs):
    app = kwargs['app']
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        use_reloader=False
    )
