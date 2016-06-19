from flaskutils import app
from flask import Flask

import json


class TestApp(object):
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
        assert 'run_tests' == app.name

    def test_render_html(self):
        """
        Makes a HTTP GET REQUEST AND GETS html
        """
        result = self.client.get('/')
        assert 200 == result.status_code
        assert b'<h1>hello world!!!</h1>' == result.get_data()

    def test_get_resource(self):
        """
        Get a Rest resource in json format
        """
        result = self.client.get('/users/1')
        assert 200 == result.status_code
        data = json.loads(result.get_data().decode('utf-8'))
        assert 'username' in data
        assert 'id' in data

    def test_get_resource_list(self):
        """
        Get a list ogf rest resources
        """
        result = self.client.get('/users')
        assert 200 == result.status_code
        data = json.loads(result.get_data().decode('utf-8'))
        assert len(data) == 2
        assert 'username' in data[0]
        assert 'id' in data[0]


    def test_post_resource(self):
        """
        Test A valid
        """

    def test_put_resource(self):
        """
        Test A valid put request
        """
        user = {'id': 1, 'username': 'userupdated', 'email': 'email@test.com'}
        response = self.client.put(
            '/users/1',
            data=json.dumps(user),
            headers=self.json_request_headers
        )
        

    def test_password_authentication(self):
        """
        valid  username and password  authentication backend
        """

    def test_token_authentication(self):
        """
        test api token authentication backend
        """

    def test_unautorized_request(self):
        """
        invalid request, user unauthorized
        """

    def test_post_rest_request(self):
        """
        create a new resource with a json request
        """

    def test_put_rest_request(self):
        """
        updating a resource using put
        """

    def test_patch_rest_request(self):
        """
        updating a resource using put
        """

    def test_delete_rest_request(self):
        """
        deleting a resource using put
        """
