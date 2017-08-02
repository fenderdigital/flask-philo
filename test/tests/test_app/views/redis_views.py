from flask import request
from flaskutils.views import BaseResourceView


class RedisView(BaseResourceView):

    def get(self, key=None):
        if key is None:
            return self.json_response(data={})
        data = self.redis_pool.get_json(key)
        if data:
            return self.json_response(data=data)
        else:
            return self.json_response(status=404)

    def post(self, key=None):
        if key is None:
            return self.json_response(status=400)
        data = request.json
        self.redis_pool.set_json(key, data)
        return self.json_response(status=201, data={'key': key})

    def delete(self, key=None):
        if key is None:
            return self.json_response(status=400)
        self.redis_pool.delete(key)
        return self.json_response(data={'key': key})
