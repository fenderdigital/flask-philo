from jsonschema import validate, FormatChecker

from .exceptions import SerializerError



class BaseSerializer(object):
    """
    Base serializer
    """
    _schema = {}

    _json = {}

    def __init__(self, request=None, model=None):
        """
        A serializer object can be built from a request object or
        a model object
        """
        if request:
            self._initialize_from_request(request)
        elif model:
            self._initialize_from_model(model)

    def _validate(self):
        # avoid extra values not defined in the schema
        if 'additionalProperties' not in self._schema:
            self._schema['additionalProperties'] = False
        validate(
            self._json, self._schema, format_checker=FormatChecker())

    def _initialize_from_request(self, request):
        """
        Loads serializer from a request object
        """
        self._json = request.json
        self._validate()
        for name, value in request.json.items():
            setattr(self, name, value)

    def _initialize_from_model(self, model):
        """
        Loads a model from
        """
        if 'properties' not in self._schema:
            raise SerializerError(
                'Can not build a serializer without a schema associated')
        else:
            _properties = self._schema['properties']

        for k, v in self.__dict__.items():
            if k in _properties:
                setattr(self, k, v)

    def to_model(self):
        """
        Builds a model based on request input
        """

    def to_json(self):
        """
        Returns a json representation
        """
        data = {}
        for k, v in self.__dict__.items():
            if not k.startswith('_'):
                data[k] =  v
        return data
