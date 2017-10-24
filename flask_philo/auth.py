from functools import wraps
from flask import request, Response
from flask_philo import app
import base64


"""
http://flask.pocoo.org/snippets/8/
This module exposes a decorator that can be used in a
flask_philo app to enforce basic auth on an endpoint.
An example of usage can be found in `test/tests/test_app/views/auth_views.py`
"""


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return (
        username == app.config['USERNAME'] and
        password == app.config['PASSWORD']
    )


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )


def requires_basic_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_string = request.headers.get('Authorization')
        if auth_string:
            auth_string = auth_string.replace('Basic ', '', 1)
            try:
                auth_string = base64.b64decode(auth_string).decode("utf-8")
                username, password = auth_string.split(':')
            except Exception:
                return authenticate()
        if not auth_string or not check_auth(username, password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
