from Hedgehog.token import *
from Hedgehog.Error import *
from Hedgehog.ast import *

class Parser:

	def __init__(self, tokens, context, filename):

		self.context = context
		self.tokens = tokens
		self.token_pos = -1

		starting = self.tokens[0].tokentrace.copy()
		starting.column = 0
		self.token = Token('SOF', ('SOF', ), starting) 
		self.prevprevtoken = Token('SOF', ('SOF', ), starting)  
		self.prevtoken = Token('SOF', ('SOF', ), starting) 
	
	def advance(self):

		if self.token_pos + 1< len(self.tokens):

			self.token_pos += 1

			self.prevprevtoken = self.prevtoken 
			self.prevtoken = self.token 
			self.token = self.tokens[self.token_pos]

		else:

			self.token = Token('EOF', ('EOF', 'OUTOFTOKENS'), self.prevtoken.tokentrace.copy())

	def unadvance(self):

		self.token = self.prevtoken 
		self.prevtoken = self.prevprevtoken 

	def look(self, size=1):

		if self.token_pos + size < len(self.tokens):

			return self.tokens[self.token_pos + size]

		else:

			return Token('EOF', ('EOF', 'OUTOFTOKENS'), self.prevtoken.tokentrace.copy())

	def parse(self):

		if len(self.tokens):

			self.advance()
			result, error = self.compoundstatement()
			if error: return None, error 
			return result, None
		else:
			return None, UnexpectedEOFError()

	def compoundstatement(self):

		self.context.traceback(Traceable(self.token.tokentrace.filename, '<statement>', self.token))
		start = self.token

		result, error = self.statementlist()
		if error: return None, error

		if not self.token.typeof('EOF', 'ENDSTATEMENT'):
			return None, ExpectingStatementEndError(self.token)

		block = StatementBlock([stmt for stmt in result], start)
		return block, None

	def statementlist(self):

		result, error = self.statement()
		if error: return None, error 

		results = [result]

		while self.token.typeof('EOL'):
			self.advance()
			
			if self.token.typeof('EOF'): return results, None

			result, error = self.statement()
			if error: return None, error 
			results.append(result)

		return results, None 

	def statement(self):

		if self.token.typeof(*IDENTIFIER, exclusive=True):
			identifier = self.token 

			if self.look().typeof(*SET, exclusive=True):
				self.advance()  # Advance to SET
				self.advance()  # Advance past SET

				assign, error = self.expression()
				if error: return None, error 

				return IdentifierAssign(identifier.value, assign, identifier), None

			else:

				result, error = self.expression()
				if error: return None, error 

				return result, None 

		else:
		
			result, error = self.expression()
			if error: return None, error

			return result, None 

	def expression(self):

		left, error = self.term()
		if error: return None, error

		while self.token.typeof('PRIORITY1'):

			op = self.token 
			self.advance()

			right, error = self.term()
			if error: return None, error 
						
			left = BinaryOp(left=left, operator=op, right=right, token=op)
			 
		return left, None 

	def term(self):

		left, error = self.highterm()
		if error: return None, error

		while self.token.typeof('PRIORITY2'):

			op = self.token 
			self.advance()

			right, error = self.highterm()
			if error: return None, error 
			
			left = BinaryOp(left=left, operator=op, right=right, token=op)

		return left, None

	def highterm(self):

		left, error = self.factor()
		if error: return None, error

		while self.token.typeof('HIGHOP'):

			op = self.token
			self.advance()

			right = None

			if op.typeof(*LPAREN, exclusive=True):

				if self.token.typeof(*RPAREN):

					self.advance()  # Advance to R parens
					right = Empty()

				else:

					right, error = self.sequence()
					if error: return None, error

					if self.token.typeof(*RPAREN, exclusive=True):
						self.advance()
					else:
						return None, HedgehogSyntaxError(')', self.token)

			elif op.typeof(*LSPAREN):

				if self.look().typeof(*RSPAREN):

					self.advance()  # Advance to RS parens
					right = Empty()

				else:

					right, error = self.expression()
					if error: return None, error

					if self.token.typeof(*RSPAREN, exclusive=True):
						self.advance()
					else:
						return None, HedgehogSyntaxError(')', self.token)

			if right is None: return None, UnexpectedTokenError(self.token)

			left = BinaryOp(left=left, operator=op, right=right, token=op)

		return left, None

	def factor(self):

		if self.token.typeof('OUTOFTOKENS'):

			return None, UnexpectedEOFError(self.token)

		elif self.token.typeof('EOL'):

			return Empty(), None

		# New Expression

		elif self.token.typeof(*LPAREN, exclusive=True):

			self.advance()

			expr, error = self.expression()
			if error: return None, error

			if self.token.typeof(*RPAREN, exclusive=True):

				self.advance()

				return expr, None

			else:

				return None, HedgehogSyntaxError(('this', 'that', 'this', 'prat'), self.token)

		# Identifier

		elif self.token.typeof(*IDENTIFIER, exclusive=True):
			identifier = self.token 
			self.advance()
			return IdentifierAccess(identifier.value, identifier), None

		# Reals

		elif self.token.typeof(*NUMBER, exclusive=True):

			number = self.token 
			self.advance()

			if int(float(number.value)) == float(number.value):

				return IntegerReal(number.value, number), None 

			else:

				return FloatReal(number.value, number), None
		
		elif self.token.typeof(*IDENTIFIER, exclusive=True):
			identifier = self.token 
			self.advance()
			return IdentifierAccess(identifier.value, identifier), None

		elif self.token.typeof(*STRING, exclusive=True):
			string = self.token
			self.advance()
			return StringReal(string.value, string), None

		# Sequences
		elif self.token.typeof(*LSPAREN, exclusive=True):
			token = self.token
			self.advance()
			listsequence, error = self.sequence()
			if error: return None, error

			if self.token.typeof(*RSPAREN, exclusive=True):

				self.advance()

				return ListSequence(listsequence, token), None

			else:

				return None, HedgehogSyntaxError(']', self.token)

		# Else

		else:

			return None, UnexpectedTokenError(self.token)

	def sequence(self):
		first, error = self.expression()
		if error: return None, error

		sequenceitems = [first]

		while self.token.typeof(*SEQ, exclusive=True):
			self.advance()  # Advance past the comma

			result, error = self.expression()
			if error: return None, error

			sequenceitems.append(result)

		return sequenceitems, None