class Traceable:

	def __init__(self, filename, locationname, token):

		self.filename = filename
		self.locationname = locationname
		self.token = token
		self.trace = self.token.tokentrace