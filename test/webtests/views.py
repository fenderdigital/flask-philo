from flask import request
from flaskutils.views import BaseView, BaseResourceView

from .serializers import (
    GetUserSerializer, PostUserSerializer, PutUserSerializer
)


class BasicHTMLView(BaseView):
    def get(self):
        return self.render_template('home.html')


class User(object):
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class UserResourceView(BaseResourceView):

    def get(self, id=None):
        if not id:
            data = [
                GetUserSerializer(
                    model=User(id=1, username='user1')).to_json(),
                GetUserSerializer(
                    model=User(id=1, username='user1')).to_json()
            ]
        else:
            data = GetUserSerializer(
                model=User(id=1, username='user1')).to_json()

        return self.json_response(data=data)

    def post(self, id):
        user = PostUserSerializer(request=request)
        return self.json_response(data=user.to_json())

    def put(self, id):
        user = PutUserSerializer(request=request)
        return self.json_response(data=user.to_json())
