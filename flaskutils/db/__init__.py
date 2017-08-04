from .postgresql.connection import initialize as init_pg
from .redis.connection import initialize as init_rd


def init_db(g, app):
    init_pg(g, app)
    init_rd(g, app)
