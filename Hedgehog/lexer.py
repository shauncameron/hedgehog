from Hedgehog.token import Token, TokenTrace, PATTERNS
from Hedgehog.Error.lexingerrors import CouldNotMatchError
import re 

class Lexer:

	@staticmethod
	def squeeze(text: str):
		result = text.rstrip()

		return result, len(text) - len(result)

	def __init__(self, filename, text):
		self.filename = filename
		self.text = text 

	def lex(self):
		tokens = []
		text = self.text 
		otext = text
		col = 0

		while len(text):
	
			matched = False
			
			for pattern, *types in PATTERNS:

				if mo := re.match(pattern, text):
					
					match = mo.group()

					tokens.append(Token(match, (pattern, *types), TokenTrace(self.filename, otext, col)))

					col += len(match)
					text = re.sub(pattern, '', text)
					
					matched = True 
					break 

			if not matched:
				
				return None, CouldNotMatchError(TokenTrace(self.filename, otext, col))

		return [token for token in tokens if not token.typeof('WHITESPACE')], None

