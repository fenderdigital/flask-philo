from flaskutils import app

from flask import Flask


class TestApp(object):
    def setup(self):
        pass

    def test_app_instanciate(self):
        """
        Test if the flask app was correctly instanciated
        """
        assert isinstance(app, Flask)

    def test_render_hmtl(self):
        """
        Makes a HTTP GET REQUEST AND GETS html
        """

    def test_get_resource(self):
        """
        Get a Rest resource in json format
        """

    def test_get_resource_list(self):
        """
        Get a list of rest resources
        """

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
