# Setup

class AST:

	pass 

class BinaryOp(AST):
	
	def __repr__(self):

		#return f'{self.left}.operator({self.operator}, {self.right})'
		return f'({self.left.value} {self.operator.value} {self.right.value})'

	def __init__(self, left, operator, right, token):

		self.left, self.right = left, right 
		self.operator = self.op = operator
		self.token = token

	@property
	def value(self):

		return self.__repr__()
	

class UnaryOp(AST):

	def __repr__(self):

		return f'Unary[{self.__class__.__name__}]'

# Reals

class NullReal(UnaryOp):

	pass 

class IntegerReal(UnaryOp):

	def __init__(self, value, token):

		self.value = value
		self.token = token

class FloatReal(UnaryOp):

	def __init__(self, value, token):

		self.value = value
		self.token = token

class StringReal(UnaryOp):

	def __init__(self, value, token):

		self.value = value
		self.token = token

class TrueReal(UnaryOp):

	def __init__(self, value, token):

		self.value = value
		self.token = token

class FalseReal(UnaryOp):

	def __init__(self, value, token):

		self.value = value
		self.token = token

# Sequences

class ListSequence(UnaryOp):

	def __init__(self, value, token):

		self.value = value
		self.token = token

class TupleSequence(UnaryOp):

	def __init__(self, value, token):

		self.value = value
		self.token = token

class Sequence(UnaryOp):

	def __init__(self, value, token):

		self.value = value
		self.token = token

# Identifier

class IdentifierAccess(UnaryOp):

	def __init__(self, identifier, token):

		self.identifier = identifier 
		self.token = token

class IdentifierAssign(UnaryOp):

	def __init__(self, identifier, item, token):

		self.identifier = identifier 
		self.item = item 
		self.token = token

# Identifier Member

class IdentifierAccessMember(UnaryOp):

	def __init__(self, identifier, member, token):

		self.identifier = identifier 
		self.member = member 
		self.token = token

class IdentifierAssignMember(UnaryOp):

	def __init__(self, identifier, member, value, token):

		self.identifier = identifier 
		self.member = member
		self.value = value
		self.token = token

# Function
class FunctionAssign(UnaryOp):

	def __init__(self, identifier, argstructure, statementblock):

		self.identifier = identifier 
		self.argstructure = argstructure
		self.statementblock = statementblock

# Class

class ClassAssign(UnaryOp):

	def __init__(self, identifier, argstructure, statementblock):

		self.identifier = identifier 
		self.argstructure = argstructure
		self.statementblock = statementblock

# Statement
		
class StatementBlock(UnaryOp):

	def __init__(self, statement_list, token):

		self.statements = self.statement_list = statement_list
		self.token = token

class BooleanExpressionStatementBlock(UnaryOp):

	def __init__(self, hhif, hhelseifs, hhelse, token):

		self.hhif = hhif 
		self.hhelseifs = hhelseifs
		self.hhelse = hhelse 
		self.token = token 

class IfStatementBlock(UnaryOp):

	def __init__(self, statementblock):

		self.statementblock = statementblock

class ElseifStatementBlock(UnaryOp):

	def __init__(self, statementblock):

		self.statementblock = statementblock

class ElseStatementBlock(UnaryOp):

	def __init__(self, statementblock):

		self.statementblock = statementblock

# Module

class IncludeModule(UnaryOp):

	def __init__(self, module, token):

		self.module = module 
		self.token = token 

# Module Utils

class Return(UnaryOp):

	def __init__(self, value):

		self.value = value 

class Stop(UnaryOp):

	pass 

class Skip(UnaryOp):

	pass

class Empty(UnaryOp):

	pass