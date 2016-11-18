from functools import wraps
from flask import request, Response
from flaskutils import app
import base64


"""
http://flask.pocoo.org/snippets/8/
"""


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return (username == app.config['USERNAME']
            and password == app.config['PASSWORD'])


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_string = request.headers.get('Authorization')
        if auth_string:
            auth_string = auth_string.replace('Basic ', '', 1)
            try:
                auth_string = base64.b64decode(auth_string).decode("utf-8")
            except:
                return("Invalid Credentials")
        username, password = auth_string.split(':')
        if not auth_string or not check_auth(username, password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
