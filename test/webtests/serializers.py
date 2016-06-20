from flaskutils.serializers import BaseSerializer


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
        },
        'required': ['email', 'username']
    }


class PutUserSerializer(BaseSerializer):
    _schema = {
        'type': 'object',
        'properties': {
            'email': {'type': 'string', 'format': 'email'},
            'username': {'type': 'string'},
            'id': {'type': 'number'}
        },
        'required': ['id', 'email', 'username']
    }
