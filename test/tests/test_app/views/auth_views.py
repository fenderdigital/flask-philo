from flask import request
from flaskutils import login_manager
from flaskutils.auth import requires_auth
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


# @login_manager.request_loader
# def load_user_from_request(request):

#     # first, try to login using the api_key url arg
#     api_key = request.args.get('api_key')
#     if api_key:
#         user = User.objects.get(api_key=api_key)
#         if user:
#             return user

#     # next, try to login using Basic Auth
#     auth_string = request.headers.get('Authorization')
#     if auth_string:
#         auth_string = auth_string.replace('Basic ', '', 1)
#         try:
#             auth_string = auth_string   # base64.b64decode(auth_string)
#         except TypeError:
#             pass
#         username, password = auth_string.split(':')
#         if (
#               username == app.config['USER']['username']
#                   and password == app.config['USER']['password']
        # ):
#             user = User.objects.get(username=username)
#         if user:
#             return user

#     # finally, return None if both methods did not login the user
#     return None


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
    @requires_auth
    def get(self):
        return self.json_response(200)
