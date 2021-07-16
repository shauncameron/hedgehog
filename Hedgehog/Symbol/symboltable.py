from Hedgehog.Error.interpretingerrors import *

class SymbolTable:
	def __init__(self, scopename, parent=None):
		self.scopename = scopename
		self.__symbols__ = {}
		self.__parentscopes__ = []
		if parent: self.__parentscopes__.append(parent)

	def get(self, name: str, trace):
		if name in self.__symbols__:
			return self.__symbols__[name], None 
		else:
			for scope in self.__parentscopes__:
				var, error = scope.get(name, trace)
				if var:
					return var, None 
			return None, HedgehogReferenceError(name, self.scopename, trace)

	def set(self, name: str, value, trace):
		self.__symbols__[name] = value 
		return value, None 
	
	def child(self, scopename: str):
		return SymbolTable(scopename, self)