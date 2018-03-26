from jinja2 import nodes
from jinja2 import lexer, nodes
from jinja2.ext import Extension


class TestExtension(Extension):
    # a set of names that trigger the extension.
    tags = set(['test_tag'])

    def __init__(self, environment):
        super(TestExtension, self).__init__(environment)


    def _test(self, msg):
        import ipdb; ipdb.set_trace()
        return '{} hello world!!!'.format(msg)

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        
        msg = ''
        for token in parser.stream:
            if token.type == 'data':
                msg = token.value
            if token.value == 'endtest_tag':
                break
            print('type {} value {}'.format(token.type, token.value) )
        #next(parser.stream)
        #msg = nodes.Const(token.value)
        call = self.call_method('_test', args=[msg], lineno=token.lineno)
        import ipdb; ipdb.set_trace()
        return nodes.Output([call], lineno=lineno)

    def parse1(self, parser):
        lineno = next(parser.stream).lineno
        token = parser.stream.expect(lexer.TOKEN_STRING)
        date_format = nodes.Const(token.value)
        call = self.call_method('_now', [date_format], lineno=lineno)
        token = parser.stream.current
        if token.test('name:as'):
            next(parser.stream)
            as_var = parser.stream.expect(lexer.TOKEN_NAME)
            as_var = nodes.Name(as_var.value, 'store', lineno=as_var.lineno)
            return nodes.Assign(as_var, call, lineno=lineno)
        else:
            return nodes.Output([call], lineno=lineno)
