from flask_philo.test import FlaskTestCase
from flask_philo import app
import json


class TestExampleEndpoints(FlaskTestCase):
    def setup(self):
        super(TestExampleEndpoints, self).setup()
        self.client = app.test_client()
        self.json_request_headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_get_example(self):
        result = self.client.get(
            '/example',
            headers=self.json_request_headers)
        # Test for valid response code
        assert 200 == result.status_code
        data = json.loads(result.get_data().decode('utf-8'))
        # Test for non-empty response JSON
        assert data != {}
