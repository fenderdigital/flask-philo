from flaskutils import app
from .models import FlaskModel
from pgsqlutils.base import syncdb, Session


class ModelTestCase(object):
    def setup(self):
        """
        Use this test case when no interaction in a view is required
        """
        syncdb()

    def teardown(self):
        Session.rollback()
        Session.close()


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
        syncdb()

    def teardown(self):
        for t in FlaskModel.metadata.sorted_tables:
            sql = 'delete from {};'.format(t.name)
            Session.execute(sql)
            Session.commit()
        Session.close()


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
