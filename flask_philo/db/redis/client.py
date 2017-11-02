class RedisClient(object):
    def __init__(self, r):
        self.r = r

    def set(self, k, v):
        self.r.set(k, v)

    def get(self, k):
        return self.r.get(k)

    def delete(self, k):
        self.r.delete(k)

    def flushdb(self):
        self.r.flushdb()

    def ping(self):
        return self.r.ping()

    def close(self):
        self.r = None
