from random import randint 
from Hedgehog.Symbol.symboltable import SymbolTable
from Hedgehog.Error import *

__symbol_ids__ = {}
n = lambda: '0x' + ''.join([f'{randint(0, 9)}' for _ in range(10)])

def hhidentify(instance):

	if not instance in __symbol_ids__:

		__symbol_ids__[instance] = n()

	return __symbol_ids__[instance]

class SymbolType(type):

	def __repr__(cls):

		return f'<Hedgehog:%s>' % cls.__name__

	def __new__(mcs, value, bases, attrs):

		return super(SymbolType, mcs).__new__(mcs, value, bases, attrs)

	# Operations

class HedgehogType:

	__metaclass__ = SymbolType

	def __init__(self, value):

		self.value = value
		self.members = SymbolTable('<EmbeddedTypeTable>')

	def __hh_add__(self, interpreter, other, trace): return None, UnsupportedOperandError('+', self.__hh_repr__(), trace)

	def __hh_min__(self, interpreter, other, trace): return None, UnsupportedOperandError('-', self.__hh_repr__(), trace)

	def __hh_div__(self, interpreter, other, trace): return None, UnsupportedOperandError('/', self.__hh_repr__(), trace)

	def __hh_mul__(self, interpreter, other, trace): return None, UnsupportedOperandError('*', self.__hh_repr__(), trace)

	def __hh_fdiv__(self, interpreter, other, trace): return None, UnsupportedOperandError('//', self.__hh_repr__(), trace)

	def __hh_pow__(self, interpreter, other, trace): return None, UnsupportedOperandError('**', self.__hh_repr__(), trace)

	# Boolean Operations

	def __hh_eq__(self, interpreter, other, trace): return None, UnsupportedOperandError('==', self.__hh_repr__(), trace)

	def __hh_neq__(self, interpreter, other, trace): return not UnsupportedOperandError('!=', self.__hh_repr__(), trace), None

	def __hh_lt__(self, interpreter, other, trace): return None, UnsupportedOperandError('<', self.__hh_repr__(), trace)

	def __hh_mt__(self, interpreter, other, trace): return not UnsupportedOperandError('>', self.__hh_repr__(), trace), None

	def __hh_lteq__(self, interpreter, other, trace): return None, UnsupportedOperandError('<=', self.__hh_repr__(), trace)

	def __hh_mteq__(self, interpreter, other, trace): return '+', self.__hh_repr__('>=', self.__hh_repr__(), trace), None

	# Boolean Results

	def __hh_bool__(self): return True

	def __hh_is__(self, interpreter, other, trace): return (other is self), None

	def __hh_and__(self, interpreter, other, trace): return (self.__hh_bool__() and other.__hh_bool__()), None

	def __hh_or__(self, interpreter, other, trace): return (self.__hh_bool__() or self.__hh_bool__()), None

	# Higher Operations

	def __hh_call__(self, interpreter, args, trace): return None, UnsupportedOperandError('call()', self.__hh_repr__(), trace)

	def __hh_setmember__(self, interpreter, member, new, trace):

		member, error = self.members.set(member, new, trace)
		if error: return None, error

		return member, None

	def __hh_getmember__(self, interpreter, member, trace):

		member, error = self.members.get(member, trace)
		if error: return None, error

		return member, None

	def __hh_setitem__(self, interpreter, item, new, trace): return None, UnsupportedOperandError('<== (setitem)', self.__hh_repr__(), trace)

	def __hh_getitem__(self, interpreter, item, trace): return None, UnsupportedOperandError('(getitem) ==>', self.__hh_repr__(), trace)

	# Repr
	
	def __hh_treerepr__(self): return f'{self.value}'

	def __hh_classrepr__(self): return f"<Hedgehog class: '{self.__class__.__name__}'>"

	def __hh_repr__(self): return f'{self.value}'

	# Types

	def __hh_str__(self, trace): return None, UnsupportedOperandError(f'str({self.__hh_repr__(), trace})', self.__hh_repr__(), trace)

	def __hh_int__(self, trace): return None, UnsupportedOperandError(f'int({self.__hh_repr__(), trace})', self.__hh_repr__(), trace)

	def __hh_float__(self, trace): return None, UnsupportedOperandError(f'float({self.__hh_repr__(), trace})', self.__hh_repr__(), trace)

	def __hh_list__(self, trace): return None, UnsupportedOperandError(f'list({self.__hh_repr__(), trace})', self.__hh_repr__(), trace)

	def __hh_tuple__(self, trace): return None, UnsupportedOperandError(f'tuple({self.__hh_repr__(), trace})', self.__hh_repr__(), trace)

	def __hh_dict__(self, trace): return None, UnsupportedOperandError(f'dict({self.__hh_repr__(), trace})', self.__hh_repr__(), trace)

	def __hh_scopetable__(self, trace): return None, UnsupportedOperandError(f'scopetable({self.__hh_repr__(), trace})', self.__hh_repr__(), trace)

class SymbolNullReal(HedgehogType):
	def __init__(self, reprval):
		super().__init__(None)
		self.reprval = reprval
	def __hh_repr__(self):
		return f'{self.reprval}'
	def __hh_bool__(self):
		return False

Null = SymbolNullReal('null')
EmptyNull = SymbolNullReal('???')

def numberdecide(value):

	if type(value) not in (float, int): raise Exception('Programming error in <numberdecide>')

	if int(float(value)) == float(value):

		return SymbolIntegerReal(value)

	else:

		return SymbolFloatReal(value)


class SymbolFloatReal(HedgehogType):
	
	def __hh_str__(self):
		
		return SymbolStringReal(f'{self.value}', trim=None)

	def __hh_float__(self):

		return self, None

	def __hh_int__(self):

		return SymbolIntegerReal(self.value)

	def __hh_add__(self, interpreter, other, trace):

		number, error = other.__hh_float__()
		if error: return None, error

		return numberdecide(self.value + other.value), None

	def __hh_min__(self, interpreter, other, trace):

		number, error = other.__hh_float__()
		if error: return None, error

		return numberdecide(self.value - other.value), None

	def __hh_div__(self, interpreter, other, trace):

		number, error = other.__hh_float__()
		if error: return None, error

		return numberdecide(self.value / other.value), None

	def __hh_mul__(self, interpreter, other, trace):

		number, error = other.__hh_float__()
		if error: return None, error

		return numberdecide(self.value * other.value), None

	def __hh_fdiv__(self, interpreter, other, trace):

		number, error = other.__hh_float__()
		if error: return None, error

		return numberdecide(self.value // other.value), None

	def __hh_pow__(self, interpreter, other, trace):

		number, error = other.__hh_float__()
		if error: return None, error

		return numberdecide(self.value ** other.value), None

	def __init__(self, value):

		value = float(value)
		super().__init__(value)

class SymbolIntegerReal(SymbolFloatReal):

	def __hh_float__(self):

		return SymbolFloatReal(self.value), None

	def __hh_int__(self):

		return self

	def __init__(self, value):

		super().__init__(value)
		self.value = int(value)

class SymbolStringReal(HedgehogType):

	def __init__(self, value, trim=(1, -1)):

		if trim:
			triml, trimr = trim 
			
			if len(value) >= 2: 
				value = value[triml:trimr]

		value = str(value)
		super().__init__(value)

one = SymbolIntegerReal(1)