from Hedgehog.lexer import Lexer 
from Hedgehog.parser import Parser
from Hedgehog.interpreter import Interpreter
from Hedgehog.token import TokenTrace
from Hedgehog.Error import HedgehogError, Traceable
from Hedgehog.Symbol.symboltable import SymbolTable
from sys import stdout, argv
from os import path

class ContextManager:

	def __init__(self, filetext, symboltablename='Globals', filename=None):

		filename = '$illusion.hh' if filename is None else filename

		self.filename, self.filetext = '<stdin, '+ filename +'>', filetext, 
		self.__tracebacks__ = []
		self.__symboltable__ = SymbolTable(symboltablename)

	def symboltable(self):
		return self.__symboltable__

	def changesymboltable(self, new):
		self.__symboltable__ = new 

	def getsymbol(self, symbolname, trace):
		result, error = self.symboltable().get(symbolname, trace)
		return result, error 

	def setsymbol(self, symbolname, symbolvalue, trace):
		result, error = self.symboltable().set(symbolname, symbolvalue, trace)
		return result, error 

	def traceback(self, add=None):

		if add is None:

			return self.__tracebacks__

		else:

			if isinstance(add, (HedgehogError, Traceable)):

				self.__tracebacks__.append(add)

			else:

				raise Exception('Cannot add non tokentrace type of object to tracebacks')
		

	def exec(self, filename=None, filetext=None):

		filename = self.filename if filename is None else filename 
		filetext = self.filetext if filetext is None else filetext

		tokens, error = Lexer(filename, filetext).lex() 
		if error:
			self.traceback(error)
			newerror = error.errortrace.copy()
			newerror.filename = '<stdin, penisville>'

			self.error(error)
			return None, error

		ast, error = Parser(tokens, self, filename).parse()
		if error:
			self.error(error)
			return None, error 

		result, error = Interpreter(self, filename).goto(ast)
		if error:
			self.error(error)
			return None, error

		return result, None 

	def error(self, error):

		errormessage, linetext, col, ln = error.e()
		message =(
			 'Hedgehog (Context Manager) $Error:' + '\n' +
			 '	Traceback (most recent call last):' + '\n' + 
'\n'.join([(('        Enter "%s", line %d, col %d:' % (tb.trace.filename, tb.trace.traceback()[2], tb.trace.column)) + '\n' + 
			 '            ' + tb.trace.traceback()[0].rstrip() + '\n'
			 '            ' + (' ' * (tb.trace.traceback()[1] - 1))) + '^' for tb in self.traceback()]) + '\n' + 
			 '    Error (%s): "%s" in "%s", line %d, col %d):' % (error.errorname, errormessage, error.errortrace.filename, ln, col) + '\n' + 
			 '        ' + linetext.rstrip() + '\n'
			 '        ' + (' ' * (col - 1)) + '^' + '\n'
			)
		stdout.write('' + message)

	def makeeof(self):

		return TokenTrace(self.filename, self.filetext, len(self.filetext) - 1)