from flaskutils import app
from pgsqlutils.base import syncdb, Session

class TransactionalTestCase(object):
    """
    Establish a database connection and create models
    """
    def setup(self):
        syncdb()

    def teardown(self):
        Session.rollback()
        Session.close()


class TestApiCase(object):
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


class TestTransactionApiCase(TransactionalTestCase):
    """
    Instanciates an http client ready to make json requests and get
    json responses, it instanciates a database connection
    """
    def setup(self):
        self.client = app.test_client()
        self.json_request_headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        super(TestTransactionApiCase, self).setup()
