from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


import sys


class Connection(object):
    def __init__(self, engine, session):
        self.engine = engine
        self.session = session


class ConnectionPool:
    """
    Flask-philo supports multiple postgresql database connections,
    this class stores one connection by every db
    """
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state

    def commit(self, connection_name='DEFAULT'):
        if connection_name is None:
            for conn_name, conn in self.connections.items():
                conn.session.commit()
        else:
            self.connections[connection_name].session.commit()

    def rollback(self, connection_name='DEFAULT'):
        if connection_name is None:
            for conn_name, conn in self.connections.items():
                conn.session.rollback()
        else:
            self.connections[connection_name].session.rollback()


pool = ConnectionPool()
pool.connections = {}


def get_pool():
    return pool


def init_db_conn(connection_name, connection_string, scopefunc=None):
    """
    Initialize a postgresql connection by each connection string
    defined in the configuration file
    """
    engine = create_engine(connection_string)
    session = scoped_session(sessionmaker(), scopefunc=scopefunc)
    session.configure(bind=engine)
    pool.connections[connection_name] = Connection(engine, session)


def initialize(g, app):
    """
    If postgresql url is defined in configuration params a
    scoped session will be created
    """
    if 'DATABASES' in app.config and 'POSTGRESQL' in app.config['DATABASES']:
        # Database connection established for console commands
        for k, v in app.config['DATABASES']['POSTGRESQL'].items():
            init_db_conn(k, v)

        if 'test' not in sys.argv:
            # Establish a new connection every request
            @app.before_request
            def before_request():
                """
                Assign postgresql connection pool to the global
                flask object at the beginning of every request
                """
                # inject stack context if not testing
                from flask import _app_ctx_stack
                for k, v in app.config['DATABASES']['POSTGRESQL'].items():
                    init_db_conn(k, v, scopefunc=_app_ctx_stack)
                g.postgresql_pool = pool

            # avoid to close connections if testing
            @app.teardown_request
            def teardown_request(exception):
                """
                Releasing connection after finish request, not required in unit
                testing
                """
                pool = getattr(g, 'postgresql_pool', None)
                if pool is not None:
                    for k, v in pool.connections.items():
                        v.session.remove()
        else:
            @app.before_request
            def before_request():
                """
                Assign postgresql connection pool to the global
                flask object at the beginning of every request
                """
                for k, v in app.config['DATABASES']['POSTGRESQL'].items():
                    init_db_conn(k, v)
                g.postgresql_pool = pool
