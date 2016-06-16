from flask import abort, json, render_template, Response
from flask.views import MethodView

from rfapp import get_app


class BaseView(MethodView):
    def __init__(self, *args, **kwargs):
        self.app = get_app()

    def json_response(self, status, **data):
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
