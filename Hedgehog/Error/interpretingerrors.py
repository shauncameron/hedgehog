from Hedgehog.Error.error import HedgehogError

class HedgehogReferenceError(HedgehogError):

	def __init__(self, symbolname, scopename, trace):

		super().__init__(HedgehogReferenceError, "'%s' in scope '%s' does not exist." % (symbolname, scopename) , trace)


class HedgehogZeroDivisionError(HedgehogError):

	def __init__(self, trace):

		super().__init__(HedgehogZeroDivisionError, "Cannot divide by Zero", trace)

class UnsupportedOperandError(HedgehogError):

	def __init__(self, op, on, trace):

		super().__init__(
			UnsupportedOperandError,
			"Unsupported operation for '%s' on '%s'" % (op, on), trace)

class UnsupportedConversionError(HedgehogError):

	def __init__(self, op, on, trace):

		super().__init__(
			UnsupportedOperandError,
			"Unsupported conversion for '%s' on '%s'" % (op, on), trace)