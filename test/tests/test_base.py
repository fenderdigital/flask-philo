from flask_philo import app
from flask import Flask


class TestAppCase(object):
    def setup(self):
        self.client = app.test_client()
        self.json_request_headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_app_instanciate(self):
        """
        Test if the flask app was correctly instanciated
        """
        assert isinstance(app, Flask)
        assert 'manage' == app.name

    def test_render_html(self):
        """
        Makes a HTTP GET REQUEST AND GETS html
        """
        result = self.client.get('/template1')
        assert 200 == result.status_code
        assert b'hello template1' == result.get_data()
        result = self.client.get('/template2')
        assert 200 == result.status_code
        assert b'hello template2' == result.get_data()
