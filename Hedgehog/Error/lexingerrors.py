from Hedgehog.Error.error import HedgehogError

class CouldNotMatchError(HedgehogError):

	def __init__(self, trace):

		super().__init__(CouldNotMatchError, 'Error whilst lexing, could not match to any pattern.', trace)