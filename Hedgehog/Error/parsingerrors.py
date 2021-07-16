from Hedgehog.Error.error import HedgehogError

class HedgehogSyntaxError(HedgehogError):

	def __init__(self, expected, token):

		if type(expected) in (list, set, tuple):

			if len(expected) > 2:
	
				message = "'" + expected[0] + "', "
				message += "', '".join(expected[1:-1]) + '"'
				message += f" or '{expected[-1]}'"

				super().__init__(SyntaxError, f"Expected {message}, instead got: '{token.value}'.", token.tokentrace)


			elif len(expected) == 2:

				super().__init__(SyntaxError, f"Expected '{expected[0]}' or '{expected[1]}', instead got: '{token.value}'.", token.tokentrace)

			else:
				
				super().__init__(SyntaxError, f"Expected '{expected[0]}', instead got: '{token.value}'.", token.tokentrace)

		else:
			
			super().__init__(SyntaxError, f'Expected "{expected}", got "{token.value}".', token.tokentrace)