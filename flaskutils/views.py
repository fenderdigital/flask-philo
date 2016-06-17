from flask import abort, json, render_template, Response
from flask.views import MethodView


class BaseView(MethodView):

    def json_response(self, status=200, data={}):
        mimetype = 'application/json'
        return Response(json.dumps(data), status=status, mimetype=mimetype)

    def render_template(self, template_name):
        return render_template(template_name)

    def get(self):
        abort(400)

    def post(self):
        abort(400)

    def put(self):
        abort(400)

    def patch(self):
        abort(400)

    def delete(self):
        abort(400)


class BaseResourceView(BaseView):

    def get(self):
        return self.json_response(400)

    def post(self):
        return self.json_response(400)

    def put(self):
        return self.json_response(400)

    def patch(self):
        return self.json_response(400)

    def delete(self):
        return self.json_response(400)
