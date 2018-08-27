from flask import g
from flask_philo import app
from flask_philo.test import FlaskTestCase
from jinja2.loaders import FileSystemLoader
from flask_philo.jinja2 import get_autoescaping_params, init_jinja2
from jinja2 import Environment, select_autoescape


class TestJinja2FileSystemLoader(FlaskTestCase):
    def get_manager(self):
        from flask_philo.jinja2 import get_manager
        # from jinja2 import get_manager
        return get_manager()

    def test_jinja2_filsystem_loader(self):
        """
        Test loader from filesystem
        """
        print("test_jinja2_filsystem_loader")
        manager = self.get_manager()
        assert 'DEFAULT' in manager.environments
        loader = manager.environments['DEFAULT'].loader
        assert FileSystemLoader == loader.__class__
        assert 3 == len(loader.list_templates())
        assert 'templates_1/index.html' == loader.list_templates()[1]
        assert 'templates_2/index.html' == loader.list_templates()[2]

    def test_load_templates(self):
        """
        test if templates are loaded correctly
        """
        manager = self.get_manager()
        env = manager.environments['DEFAULT']
        template_idx1 = env.get_template('templates_1/index.html')
        template_idx2 = env.get_template('templates_2/index.html')
        idx1 = template_idx1.render({'msg_1': 'hello template1'})
        idx2 = template_idx2.render({'msg_2': 'hello template2'})
        assert idx1 == 'hello template1'
        assert idx2 == 'hello template2'

    def test_request_context(self):
        manager = self.get_manager()
        ctx = app.test_request_context('/hello-template')
        manager.set_request(ctx.request)
        env = manager.environments['DEFAULT']
        assert 'FLASK_PHILO_CONFIG' in env.globals
        assert env.globals['REQUEST'].path == '/hello-template'

    def test_custom_tag(self):
        manager = self.get_manager()
        env = manager.environments['DEFAULT']
        template = env.get_template('home.html')
        txt = template.render()
        assert 'random_msg hello world!!!' == txt

    def test_init(self):
        init_jinja2(g, app)

        assert hasattr(app, 'jinja_env')
        assert hasattr(app, 'jinja_options')
        assert hasattr(app, 'jinja_loader')
        assert hasattr(app, 'jinja_environment')


    # def test_autoescaping(self):
        # manager = self.get_manager()
        # params = get_autoescaping_params(**app.config)
        # print("params : ", params)

        # env = Environment(
            # autoescape=select_autoescape(**params),
        # )
        # env = manager.environments['DEFAULT']
        # print("env : ", env)


        # import ipdb; ipdb.set_trace()


        # template_idx1 = env.get_template('templates_1/index.html')
        # idx1 = template_idx1.render({'msg_1': 'hello template1'})
        # assert idx1 == 'hello template1'
