from flaskutils import app
from .models import FlaskModel

from pgsqlutils.base import syncdb, init_db_conn


class ModelTestCase(object):
    def setup(self):
        """
        Use this test case when no interaction in a view is required
        """
        if 'POSTGRESQL_DATABASE_URI' in app.config:
            self.PGSession = init_db_conn()
            syncdb()

    def teardown(self):
        if 'POSTGRESQL_DATABASE_URI' in app.config:
            self.PGSession.rollback()


class TransactionalTestCase(object):
    """
    This tests should be used when testing views
    """
    def setup(self):
        self.client = app.test_client()
        self.json_request_headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        if 'POSTGRESQL_DATABASE_URI' in app.config:
            self.PGSession = init_db_conn()
            syncdb()

    def teardown(self):
        if 'POSTGRESQL_DATABASE_URI' in app.config:
            for t in reversed(FlaskModel.metadata.sorted_tables):
                sql = 'delete from {} cascade;'.format(t.name)
                self.PGSession.execute(sql)
                self.PGSession.commit()


class ApiTestCase(object):
    """
    Instanciates an http client ready to make json requests and get
    json responses, it doesn't instanciate a database connection
    """
    def setup(self):
        self.client = app.test_client()
        self.json_request_headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
