from flaskutils import app
from flaskutils.db.postgresql.orm import BaseModel
from flaskutils.db.postgresql import syncdb
from flaskutils.db.postgresql.connection import get_pool


class FlaskTestCase(object):
    """
    This tests should be used when testing views
    """
    def setup(self):
        self.client = app.test_client()
        self.json_request_headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        if 'DATABASES' in app.config and\
                'POSTGRESQL' in app.config['DATABASES']:
            self.postgresql_pool = get_pool()
            syncdb()

    def teardown(self):
        if 'DATABASES' in app.config and 'POSTGRESQL'\
                in app.config['DATABASES']:
            for t in reversed(BaseModel.metadata.sorted_tables):
                sql = 'delete from {} cascade;'.format(t.name)
                for c_name, conn in self.postgresql_pool.connections.items():
                    conn.session.execute(sql)
                    conn.session.commit()
