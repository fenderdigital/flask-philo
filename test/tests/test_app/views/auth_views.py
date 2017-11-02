from flask_philo.auth import requires_basic_auth
from flask_philo.views import BaseView


class RequiresBasicAuthView(BaseView):
    @requires_basic_auth
    def get(self):
        return self.json_response(200)
