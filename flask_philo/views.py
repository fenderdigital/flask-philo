from flask_philo import app
from flask import abort, json, render_template, make_response, Response, g
from flask.views import MethodView


class BaseView(MethodView):
    def __init__(self, *args, **kwargs):

        # assign postgresql pool connections
        if 'DATABASES' in app.config and\
                'POSTGRESQL' in app.config['DATABASES']:
            if hasattr(g, 'postgresql_pool'):
                self.postgresql_pool = g.postgresql_pool

        # assign redis pool connections
        if 'DATABASES' in app.config and 'REDIS' in app.config['DATABASES']:
            if hasattr(g, 'redis_pool'):
                self.redis_pool = g.redis_pool

        if 'JINJA2_TEMPLATES' in app.config:
            if hasattr(g, 'jinja2_template_manager'):
                self.jinja2_template_manager = g.jinja2_template_manager
        super(BaseView, self).__init__(*args, **kwargs)

    def json_response(self, status=200, data={}, headers={}):
        mimetype = 'application/json'

        header_dict = {}
        for k, v in headers.items():
            header_dict[k] = v

        return Response(
            json.dumps(data),
            status=status,
            mimetype=mimetype,
            headers=header_dict)

    def render_template(self, template_name, engine_name='DEFAULT', **values):
        if not hasattr(self, 'jinja2_template_manager'):
            return render_template(template_name, **values)
        else:
            return self.jinja2_template_manager.render(
                template_name, **values)

    def template_response(self, template_name, headers={}, **values):
        """
        Constructs a response, allowing custom template name and content_type
        """
        response = make_response(
            self.render_template(template_name, **values))

        for field, value in headers.items():
            response.headers.set(field, value)

        return response

    def get(self, *args, **kwargs):
        abort(400)

    def post(self, *args, **kwargs):
        abort(400)

    def put(self, *args, **kwargs):
        abort(400)

    def patch(self, *args, **kwargs):
        abort(400)

    def delete(self, *args, **kwargs):
        abort(400)


class BaseResourceView(BaseView):

    def get(self, *args, **kwargs):
        return self.json_response(400)

    def post(self, *args, **kwargs):
        return self.json_response(400)

    def put(self, *args, **kwargs):
        return self.json_response(400)

    def patch(self, *args, **kwargs):
        return self.json_response(400)

    def delete(self, *args, **kwargs):
        return self.json_response(400)
