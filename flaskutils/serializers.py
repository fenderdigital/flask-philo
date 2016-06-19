from jsonschema import validate


class BaseSerializer(object):
    """
    Base serializer
    """
    model = None

    schema = {}

    def __init__(self, request, **kwargs):
        self._request = request
        import ipdb; ipdb.set_trace()

    def from_model(self):
        """
        Loads a model from 
        """

    def to_model(self):
        """
        Builds a model based on request input
        """
