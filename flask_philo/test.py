from flask_philo import app
from flask_philo.db.postgresql.orm import BaseModel
from flask_philo.db.postgresql import syncdb
from flask_philo.db.postgresql.connection import get_pool
from flask_philo.db.redis.connection import get_pool as get_redis_pool
from flask_philo.db.elasticsearch.connection import get_pool as get_el_pool


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

        if 'DATABASES' in app.config and 'REDIS' in app.config['DATABASES']:
            self.redis_pool = get_redis_pool()

        if 'DATABASES' in app.config and\
                'ELASTICSEARCH' in app.config['DATABASES']:
            self.elasticsearch_pool = get_el_pool()

    def teardown(self):
        if 'DATABASES' in app.config and 'POSTGRESQL'\
                in app.config['DATABASES']:
            for t in reversed(BaseModel.metadata.sorted_tables):
                sql = 'delete from {} cascade;'.format(t.name)
                for c_name, conn in self.postgresql_pool.connections.items():
                    conn.session.execute(sql)
                    conn.session.commit()

        if 'DATABASES' in app.config and 'REDIS' in app.config['DATABASES']:
            self.redis_pool.flushall()

        if 'DATABASES' in app.config and\
                'ELASTICSEARCH' in app.config['DATABASES']:
            self.elasticsearch_pool.flushall()
            for c_name, conn in self.elasticsearch_pool.connections.items():
                for idx in conn.get_alias():
                    conn.delete_index(idx)
