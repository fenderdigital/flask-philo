from flaskutils.serializers import BaseSerializer


class GetUserSerializer(BaseSerializer):
    """
    Used to serialize get resopnses
    """
    _schema = {
        'type': 'object',
        'properties': {
            'id': {'type': 'number'},
            'email': {'type': 'string', 'format': 'email'},
            'username': {'type': 'string'},
            'last_login': {'type': 'string', 'format': 'date-time'},
            'birthday': {'type': 'string', 'format': 'date'},
        }
    }


class PostUserSerializer(BaseSerializer):
    """
    Post requests don't required id as they mean to be
    used for create new objects
    """
    _schema = {
        'type': 'object',
        'properties': {
            'email': {'type': 'string', 'format': 'email'},
            'username': {'type': 'string'},
            'last_login': {'type': 'string', 'format': 'date-time'},
            'birthday': {'type': 'string', 'format': 'date'},
            'password': {'type': 'string'},
        },
        'required': ['email', 'username', 'password']
    }


class PutUserSerializer(BaseSerializer):
    _schema = {
        'type': 'object',
        'properties': {
            'email': {'type': 'string', 'format': 'email'},
            'username': {'type': 'string'},
            'id': {'type': 'number'},
            'last_login': {'type': 'string', 'format': 'date-time'},
            'password': {'type': 'string'},
        },
        'required': ['id', 'email', 'username']
    }



class LoginSerializer(BaseSerializer):
    """
    Post requests with login credentials
    """
    _schema = {
        'type': 'object',
        'properties': {
            'username': {'type': 'string'},
            'password': {'type': 'string'},
            'email': {'type': 'string', 'format': 'email'}
        },
        'required': ['email', 'username', 'password']
    }
