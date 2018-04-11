from datetime import date, datetime
from decimal import Decimal
from jsonschema import validate, FormatChecker

from flask_philo import utils
from .exceptions import SerializerError
import uuid

# uuid
uuid_schema = {
    "type": "string",
    "pattern": "^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$"  # noqa
}


decimal_schema = {
    "type": "string",
    "pattern": "\d+\.\d+"
}


class BaseSerializer(object):
    """
    Base serializer
    """
    _schema = {}

    _json = {}

    __model__ = None

    def __init__(self, request=None, model=None, data=None):
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
            self._initialize_from_dict(request.json)
        elif model:
            self._initialize_from_model(model)
        elif data:
            self._initialize_from_dict(data)
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

    def _initialize_from_dict(self, data):
        """
        Loads serializer from a request object
        """
        self._json = data
        self._validate()

        for name, value in self._json.items():
            if name in self._properties:
                if '$ref' in self._properties[name]:
                    if 'decimal' in self._properties[name]['$ref']:
                        value = Decimal(value)

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

    def update(self):
        """
        Finds record and update it based in serializer values
        """
        obj = self.__model__.objects.get_for_update(id=self.id)
        for name, value in self.__dict__.items():
            if name in self._properties:
                setattr(obj, name, value)
        obj.update()
        return obj

    def to_json(self):
        """
        Returns a json representation
        """
        data = {}
        for k, v in self.__dict__.items():
            if not k.startswith('_'):
                # values not serializable, should be converted to strings
                if isinstance(v, datetime):
                    v = utils.datetime_to_string(v)
                elif isinstance(v, date):
                    v = utils.date_to_string(v)
                elif isinstance(v, uuid.UUID):
                    v = str(v)
                elif isinstance(v, Decimal):
                    v = str(v)
                data[k] = v
        return data
