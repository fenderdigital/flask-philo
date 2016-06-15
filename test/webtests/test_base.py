from flaskutils import get_app


class TestApp(object):
    def test_app_instanciate(self):
        """
        Test if the flask app was correctly instanciated
        """
        app = get_app()
        import ipdb; ipdb.set_trace()
