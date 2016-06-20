from flask import request
from flaskutils.views import BaseView, BaseResourceView
from flaskutils import app

from .serializers import UserSerializer

class BasicHTMLView(BaseView):
    def get(self):
        return self.render_template('home.html')


class UserResourceView(BaseResourceView):

    def get(self, id=None):
        if not id:
            data = [
                {'id': 1, 'username': 'user1'},
                {'id': 2, 'username': 'user2'}
            ]
        else:
            data = {'id': 1, 'username': 'user1'}

        return self.json_response(data=data)

    def post(self, id):
        user = UserSerializer(request)
        return self.json_response(data=user.to_json)

    def put(self, id):
        user = UserSerializer(request)
        return self.json_response()
