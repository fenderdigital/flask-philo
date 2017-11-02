from .postgresql.connection import initialize as init_pg
from .redis.connection import initialize as init_rd
from .elasticsearch.connection import initialize as init_el


def init_db(g, app):
    init_pg(g, app)
    init_rd(g, app)
    init_el(g, app)
