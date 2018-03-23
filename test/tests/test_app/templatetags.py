from jinja2 import nodes
from jinja2.ext import Extension


class TestExtension(Extension):
    # a set of names that trigger the extension.
    tags = set(['test_tag'])

    def __init__(self, environment):
        super(TestExtension, self).__init__(environment)

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        import ipdb; ipdb.set_trace()
        args = [parser.parse_expression()]
        body = 'aaaa'

        
        while parser.stream.current.type != 'block_end':
            print(parser.parse_expression())
        return nodes.CallBlock(self.call_method('_test_tag', args),
                               [], [], body).set_lineno(lineno)

    def _test_tag(self, name, caller):
        import ipdb; ipdb.set_trace()
        return 'hello world!!!'
