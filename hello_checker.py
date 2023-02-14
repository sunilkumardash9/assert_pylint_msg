from pylint import interfaces,lint, checkers
import tokenize


class HelloWorldTokenChecker(checkers.BaseChecker):
    __implements__ = interfaces.ITokenChecker

    name = 'hello-world-token'
    priority = -1
    msgs = {
        'C9002': (
            'Uses a "Hello, world!" string.',
            'hello-world-token',
            'No code should use "Hello, world!" statements.',
        ),
    }
    def process_tokens(self, tokens):
        for token in tokens:
            if token.type == tokenize.STRING:
                quotes_stripped = token.string.strip('"').strip('\'')
                if quotes_stripped == 'hello world':
                    self.add_message('hello-world-token', line=token.start[0])

def register(linter: lint.PyLinter):
    linter.register_checker(HelloWorldTokenChecker(linter))

