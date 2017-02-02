from flask import abort, json, render_template, Response
from flask.views import MethodView


class BaseView(MethodView):

    def json_response(self, status=200, data={}):
        mimetype = 'application/json'
        return Response(json.dumps(data), status=status, mimetype=mimetype)

    def render_template(self, template_name, **values):
        return render_template(template_name, **values)

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
