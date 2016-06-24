from pgsqlutils.orm import BaseModel


class FlaskModel(BaseModel):
    __abstract__ = True

    def __init__(self, **kwargs):
        if 'serializer' not in kwargs:
            super(FlaskModel, self).__init__(**kwargs)
        else:
            # checks if data came from a serializer
            serializer = kwargs['serializer']
            params = {}
            for k, v in serializer.__dict__.items():
                if not k.startswith('_'):
                    params[k] = v
            super(FlaskModel, self).__init__(**params)
