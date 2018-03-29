from jinja2 import nodes
from jinja2.ext import Extension


class TestExtension(Extension):
    # a set of names that trigger the extension.
    tags = set(['testtag'])

    def __init__(self, environment):
        super(TestExtension, self).__init__(environment)

    def _testtag(self, msg, caller):
        return '{} hello world!!!'.format(msg)

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        args = [parser.parse_expression()]
        body = parser.parse_statements(['name:endtesttag'], drop_needle=True)
        return nodes.CallBlock(
            self.call_method(
                '_testtag', args), [], [], body).set_lineno(lineno)
