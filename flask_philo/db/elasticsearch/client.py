from elasticsearch.helpers import bulk


class ElasticSearchClient(object):
    def __init__(self, el):
        self.el = el
        # import ipdb; ipdb.set_trace()

    def ping(self):
        return self.el.ping()

    def create_index(self, name):
        return self.el.indices.create(name)

    def index(self, index=None, doc_type=None, id=None, body=None):
        return self.el.index(index=index, doc_type=doc_type, id=id, body=body)

    def bulk_index(self, data=None, index=None, doc_type=None):
        actions = []
        for item in data:
            it = {}
            it['_id'] = item['id']
            it['_op_type'] = 'index'
            it['_type'] = doc_type
            for k, v in item.items():
                it[k] = v
            actions.append(it)
        bulk(self.el, actions, index=index)

    def delete_index(self, name):
        self.el.indices.delete(name)

    def count(self, name):
        return self.el.count(name).get('count', 0)

    def delete(self, idx, doc_type, id):
        self.el.delete(idx, doc_type=doc_type, id=id)

    def get_alias(self, name=None):
        return self.el.indices.get_alias(name)

    def get(self, index=None, doc_type=None, id=None):
        return self.el.get(index=index, doc_type=doc_type, id=id)

    def get_connection(self):
        return self.el

    def flush(self):
        self.el.indices.flush()

    def search(self, **kwargs):
        return self.el.search(**kwargs)

    def close(self):
        self.el = None
