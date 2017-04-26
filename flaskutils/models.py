from pgsqlutils.orm import BaseModel


class FlaskModel(BaseModel):
    __abstract__ = True

    def __init__(self, **kwargs):
        super(FlaskModel, self).__init__(**kwargs)
