from flask import request
from flaskutils import app
from flaskutils.views import BaseView
from flaskutils.exceptions import AuthenticationError
from jsonschema.exceptions import ValidationError

from tests.test_app.models import User
from tests.test_app.serializers import (
    LoginSerializer
)

import flask_login


class LoginView(BaseView):
    def post(self):
        data = {}

        try:
            serializer = LoginSerializer(
                request=request)
            user = User.authenticate(
                password=serializer.password, email=serializer.email,
                username=serializer.username)
            flask_login.login_user(user)

            return self.json_response(
                200, data={'username': user.username})

        except ValidationError as e:
            data = {'msg': e.message}

        except AuthenticationError as e:
            data = {'msg': str(e)}

        return self.json_response(status=401, data=data)
