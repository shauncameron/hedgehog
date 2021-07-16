from Hedgehog.Error.error import HedgehogError

class ExpectingStatementEndError(HedgehogError):

	def __init__(self, token):

		super().__init__(ExpectingStatementEndError, f'Expecting a statement ender, instead got "{token.value}".', token.tokentrace)

class UnexpectedEOFError(HedgehogError):

	def __init__(self, token):

		super().__init__(UnexpectedEOFError, f'Encountered unexpected EOF.', token.tokentrace)

class UnexpectedTokenError(HedgehogError):

	def __init__(self, token):

		super().__init__(UnexpectedTokenError, f'Encountered unexpected token type(%s).' % token.type(), token.tokentrace)