from flask import request
from flaskutils import login_manager
from flaskutils.auth import requires_basic_auth
from flaskutils.views import BaseView
from flaskutils.exceptions import AuthenticationError
from jsonschema.exceptions import ValidationError

from tests.test_app.models import User
from tests.test_app.serializers import (
    LoginSerializer
)
from flask_login import login_user, logout_user, login_required


@login_manager.user_loader
def load_user(id):
    """
    If user does not exist should return None
    """
    try:
        return User.objects.get(id=id)
    except:
        pass


class LoginView(BaseView):
    def post(self):
        data = {}
        try:
            serializer = LoginSerializer(
                request=request)
            user = User.authenticate(
                password=serializer.password, email=serializer.email,
                username=serializer.username)
            login_user(user)

            return self.json_response(
                200, data={'username': user.username})

        except ValidationError as e:
            data = {'msg': e.message}

        except AuthenticationError as e:
            data = {'msg': str(e)}

        return self.json_response(status=401, data=data)


class LogoutView(BaseView):
    @login_required
    def post(self):
        logout_user()
        return self.json_response(200)


class ProtectectView(BaseView):
    @login_required
    def get(self):
        return self.json_response(200)


class RequiresBasicAuthView(BaseView):
    @requires_basic_auth
    def get(self):
        return self.json_response(200)
