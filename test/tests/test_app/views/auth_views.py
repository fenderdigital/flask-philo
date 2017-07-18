from flaskutils.auth import requires_basic_auth
from flaskutils.views import BaseView


class RequiresBasicAuthView(BaseView):
    @requires_basic_auth
    def get(self):
        return self.json_response(200)
