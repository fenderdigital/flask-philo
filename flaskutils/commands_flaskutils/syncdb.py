from flaskutils.db.postgresql import syncdb


def run(*args, **kwargs):
    syncdb()
