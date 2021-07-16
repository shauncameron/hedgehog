from Hedgehog.Error.nonerror import Traceable

class HedgehogError(Traceable):

	def __init__(self, errorclass, errormessage, errortrace, errortoken=None):
		self.errorname = errorclass.__name__ 
		self.errormessage, self.errortrace, self.errotoken = errormessage, errortrace, errortoken
		
		# To qualify as a traceback
		self.trace = self.errortrace
		self.message = self.errormessage

	def e(self):

		return self.errormessage, *self.errortrace.traceback()