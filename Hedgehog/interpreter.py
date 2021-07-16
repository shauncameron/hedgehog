from Hedgehog.token import *
from Hedgehog.Symbol import *

class Interpreter:

	def __init__(self, context, filename):
		self.context = context
		self.filename = filename

	def error(self, node):
		raise Exception(f'Python interpretation error({node.__class__.__name__})')

	def goto(self, node):
		visit = getattr(self, 'goto' + node.__class__.__name__, self.error)

		result, error = visit(node)
		if error: return None, error

		return result, None

	def gotoStatementBlock(self, node):
		if len(node.statements):

			for statement in node.statements:

				result, error = self.goto(statement)
				if error: return None, error

			return result, None

		raise Exception('Take this exception in lue of a Null')

	def gotoBinaryOp(self, node):

		if node.op.typeof(*PLUS, exclusive=True):

			left, error = self.goto(node.left)
			if error: return None, error 

			right, error = self.goto(node.right)
			if error: return None, error

			result, error = left.__hh_add__(self, right, node.token.tokentrace)
			if error: return None, error

			return result, None

		if node.op.typeof(*MINUS, exclusive=True):

			left, error = self.goto(node.left)
			if error: return None, error 

			right, error = self.goto(node.right)
			if error: return None, error

			result, error = left.__hh_min__(self, right, node.token.tokentrace)
			if error: return None, error

			return result, None

		if node.op.typeof(*DIV, exclusive=True):

			left, error = self.goto(node.left)
			if error: return None, error 

			right, error = self.goto(node.right)
			if error: return None, error

			result, error = left.__hh_div__(self, right, node.token.tokentrace)
			if error: return None, error

			return result, None

		if node.op.typeof(*MUL, exclusive=True):

			left, error = self.goto(node.left)
			if error: return None, error 

			right, error = self.goto(node.right)
			if error: return None, error

			result, error = left.__hh_mul__(self, right, node.token.tokentrace)
			if error: return None, error

			return result, None

		if node.op.typeof(*FLOORDIV, exclusive=True):

			left, error = self.goto(node.left)
			if error: return None, error 

			right, error = self.goto(node.right)
			if error: return None, error

			result, error = left.__hh_fdiv__(self, right, node.token.tokentrace)
			if error: return None, error

			return result, None

		if node.op.typeof(*POW, exclusive=True):

			left, error = self.goto(node.left)
			if error: return None, error 

			right, error = self.goto(node.right)
			if error: return None, error

			result, error = left.__hh_pow__(self, right, node.token.tokentrace)
			if error: return None, error

			return result, None

		if node.op.typeof('CALLOPEN'):

			left, error = self.goto(node.left)
			if error: return None, error

			args, error = self.goto(node.right)
			if error: return None, error

			result, error = left.__hh_call__(self, args, node.token.tokentrace)
			if error: return None, error

			return result, None

		else:

			raise Exception('WHY ARE YOU HERE')

	# Identifier
	def gotoIdentifierAccess(self, node):
		result, error = self.context.getsymbol(node.identifier, node.token.tokentrace)
		if error: return None, error 
		
		return result, None

	def gotoIdentifierAssign(self, node):
		result, error = self.goto(node.item)
		if error: return None, error
		
		result, error = self.context.setsymbol(node.identifier, result, node.token.tokentrace)
		
		return result, None

	# Reals	

	def gotoFloatReal(self, node):
		return SymbolFloatReal(node.value), None

	def gotoIntegerReal(self, node):
		return SymbolIntegerReal(node.value), None

	def gotoStringReal(self, node):
		return SymbolStringReal(node.value), None

	def gotoTupleSequence(self, node):
		results = []
		seq = node.value

		for expr in seq:
			result, error = self.goto(expr)
			if error: return None, error

			results.append(result)

		return SymbolTupleSequence(results), None

	def gotoListSequence(self, node):
		results = []
		seq = node.value

		for expr in seq:
			result, error = self.goto(expr)
			if error: return None, error

			results.append(result)

		return SymbolListSequence(results), None

	def gotoNull(self, node):
		return Null, None

	def gotoEmpty(self, node):
		return EmptyNull, None