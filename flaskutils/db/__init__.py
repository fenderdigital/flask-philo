from .postgresql.connection import initialize as init_pg


def init_db(g, app):
    init_pg(g, app)
