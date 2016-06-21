from datetime import date, datetime
from jsonschema import validate, FormatChecker

from flaskutils import utils
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

        if 'properties' not in self._schema:
            raise SerializerError(
                'Can not build a serializer without a schema associated')
        else:
            self._properties = self._schema['properties']

        if request:
            self._initialize_from_request(request)
        elif model:
            self._initialize_from_model(model)
        else:
            raise SerializerError(
                'Can not build a serializer without an'
                'http request or model associated')

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
            if name in self._properties:
                # applying proper formatting when required
                if 'format' in self._properties[name]:
                    format = self._properties[name]['format']

                    if 'date-time' == format:
                        value = utils.string_to_datetime(value)
                    elif 'date' == format:
                        value = utils.string_to_date(value)
                setattr(self, name, value)

    def _initialize_from_model(self, model):
        """
        Loads a model from
        """
        for name, value in model.__dict__.items():
            if name in self._properties:
                setattr(self, name, value)

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
                # dates are not serializable, should be converted to strings
                if isinstance(v, datetime):
                    v = utils.datetime_to_string(v)
                elif isinstance(v, date):
                    v = utils.date_to_string(v)
                data[k] = v
        return data
