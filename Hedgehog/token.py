class TokenTrace:

	def __repr__(self):
		return """TokenTrace[ @col%d ]""" % self.column

	def __init__(self, filename, text, column):
		self.filename = filename
		self.text = text 
		self.column = column 

	def traceback(self):
		line = 0 
		linetext = ''
		cols = 0

		resultingline = None 
		
		for col, char in enumerate(self.text):

			if line == resultingline:

				break

			linetext += char 
			
			if resultingline is None:
				
				cols += 1

			if col == self.column:

				resultingline = line + 1

			elif char == '\n':

				line += 1

				if resultingline is None:

					cols = 0
					linetext = ''

		return linetext, cols, line

	def copy(self):

		return TokenTrace(self.filename, self.text, self.column)

class Token:

	def __repr__(self):

		return f"""Token[{self.tokentrace.column}]={[self.value]}"""

	def type(self):

		return self.types[1]

	def typeof(self, *types, searchof=None, exclusive=False):

		if searchof is None:

			if exclusive:

				res = []
				for t in types:
					res.append(t in self.types)

				return False not in [t in self.types for t in types]
		

			else:

				return True in [t in self.types for t in types]

		else:

			return True if types[searchof] in self.types else False

	def __init__(self, value, types, tokentrace):
		self.value = value 
		self.types = types 
		self.tokentrace = tokentrace

	def copy(self, copytokentrace=True):

		if copytokentrace:

			return Token(self.value, self.types, self.tokentrace.copy())

		else:

			return Token(self.value, self.types, self.tokentrace)

PATTERNS = (
	# Statement Block Keywords
	CLASSKW := (r'^class', 'CLASSKW', 'KEYWORD'),
	FUNCKW := (r'^func', 'FUNCKW', 'KEYWORD'),
	STATEMENTKW := (r'^statement', 'STATEMENTKW', 'KEYWORD'),
	# Boolean Expression Keywords
	IFKW := (r'^if', 'IFKW', 'KEYWORD'),
	ELSEIFKW := (r'^elseif', 'ELSEIFKW', 'KEYWORD'),
	ELIFKW := (r'^elif', 'ELSEIFKW', 'KEYWORD'),
	ELSEKW := (r'^else', 'ELSEKW', 'KEYWORD'),
	# Variable Declaration Keywords
	LOCAKW := (r'^local', 'LOCALKW', 'KEYWORD'),
	GLOBALKW  := (r'^global', 'GLOBALKW', 'KEYWORD'),
	UPPERKW := (r'^upper', 'UPPERKW', 'KEYWORD'),	
	# Error handling Keywords
	TRYKW := (r'^try', 'TRYKW', 'KEYWORD'),
	CATCHKW := (r'^catch', 'CATCHKW', 'KEYWORD'),
	FINALLYKW := (r'^finally', 'FINALLKW', 'KEYWORD'),
	THROWKW := (r'^throw', 'THROWKW', 'KEYWORD'),
	# Module Keywords
	PACKAGEKW := (r'^package', 'PACKAGEKW', 'KEYWORD'),
	INCLUDINGKW := (r'^including', 'INCLUDINGKW', 'KEYWORD'),
	INCLUDEKW := (r'^include', 'INCLUDEKW', 'KEYWORD'),
	FROMKW := (r'^from', 'FROMKW', 'KEYWORD'),
	# Reserved Keywords
	TRUEKW := (r'^true', 'TRUEKW', 'RESERVED', 'KEYWORD'),
	FALSEKW := (r'^false', 'FALSEKW', 'RESERVED', 'KEYWORD'),
	NULLKW := (r'^null', 'NULLKW', 'RESERVED', 'KEYWORD'),
	# Parentheses
	LPAREN := (r'^\(', 'LPAREN', 'CALLOPEN', 'HIGHOP'),
	RPAREN := (r'^\)', 'RPAREN', 'SEQTERMINATOR'),
	LSPAREN := (r'^\[', 'LSPAREN', 'GETITEM', 'HIGHOP'),
	RSPAREN := (r'^\]', 'RSPAREN', 'SEQTERMINATOR'),
	LCPAREN := (r'^\{', 'LCPAREN', 'DICTOPEN'),
	RCPAREN := (r'^\}', 'RCPAREN', 'SEQTERMINATOR', 'ENDSTATEMENT'),
	# Data Types
	NUMBER := (r'^-?[0-9]+(?:\.[0-9]+)?', 'NUM', 'LITERAL', 'FACTOR'),
	STRING := (r'^"([\s\S]*?[^\\])"', 'STR', 'LITERAL', 'FACTOR'),
	THINSTRING := (r"'([\s\S]*?[^\\])'", 'STR', 'LITERAL', 'FACTOR'),
	# Identifier
	IDENTIFIER := (r'^[a-zA-Z0-9_]+[a-zA-Z0-9_]*', 'IDT', 'IDENTIFIER', 'FACTOR'),
	# Operators
	EQ := (r'^==', 'EQ', 'OP', 'PRIORITY2'),
	NEQ := (r'^!=', 'NEQ', 'OP', 'PRIORITY2'),
	LTEQ := (r'^<=', 'LTEQ', 'OP', 'PRIORITY2'),
	MTEQ := (r'^>=', 'MTEQ', 'OP', 'PRIORITY2'),
	LT := (r'^<', 'LT', 'OP', 'PRIORITY2'),
	MT := (r'^>', 'MT', 'OP', 'PRIORITY2'),
	AND := (r'^&&', 'AND', 'OP', 'PRIORITY2'),
	OR := (r'^\|\|', 'OR', 'OP', 'PRIORITY2'),
	PLUS := (r'^\+', 'PLUS', 'OP', 'PRIORITY1'),
	MINUS := (r'^-', 'MINUS', 'OP', 'PRIORITY1'),
	POW := (r'^\*\*', 'POW', 'OP', 'PRIORITY2'),
	FLOORDIV := (r'^\/\/', 'FLOORDIV', 'OP', 'PRIORITY2'),
	DIV := (r'^\/', 'DIV', 'OP', 'PRIORITY2'),
	MUL := (r'^\*', 'MUL', 'OP', 'PRIORITY2'),
	MODULO := (r'^%', 'MOD', 'MUDULO', 'PRIORITY2'),
	# Other Operators
	DOT := (r'^\.', 'DOT', 'HIGHOP'),
	# Other
	SET := (r'^=', 'SET'),
	WRSET := (r'^:=', 'WRSET'),
	SEQ := (r'^,', 'SEQ', ),
	WHITESPACEN := (r'^\s', 'WHITESPACE', ),
	WHITESPACEP := (r'^ ', 'WHITESPACE', ),
	EOL := (r'^;', 'EOL', ),
)