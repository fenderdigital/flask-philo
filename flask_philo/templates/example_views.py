from flask_philo.views import BaseResourceView


class ExampleView(BaseResourceView):
    def get(self):
        return self.json_response(
            status=200, data={'some_data': 'yes'})
