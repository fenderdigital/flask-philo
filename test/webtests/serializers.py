from flaskutils.serializers import BaseSerializer


class UserSerializer(BaseSerializer):
    schema = {
        "$schema": "http://json-schema.org/schema#",
        'type': 'object',
        'properties': {
            'email': {'type': 'string', 'format': 'email'},
            'username': {'type': 'string'},
            'id': {'type': 'number'}
        },
        'required': ['id', 'email', 'username']
    }
