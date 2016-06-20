from jsonschema import validate, FormatChecker


class BaseSerializer(object):
    """
    Base serializer
    """
    model = None

    schema = {}

    def __init__(self, request, **kwargs):
        self._request = request
        self._validate()

        for name, value in self._request.json.items():
            setattr(self, name, value)

    def _validate(self):
        # avoid extra values not defined in the schema
        if 'additionalProperties' not in self.schema:
            self.schema['additionalProperties'] = False

        self.is_valid = validate(
            self._request.json, self.schema, format_checker=FormatChecker())

    def from_model(self):
        """
        Loads a model from
        """

    def to_model(self):
        """
        Builds a model based on request input
        """

    def to_json(self):
        """
        Returns a json representation
        """
        data = {}
        for v in dir(self):
            if not v.startswith('_'):
                value = getattr(self, v)
                data[v] =  value
        return data
