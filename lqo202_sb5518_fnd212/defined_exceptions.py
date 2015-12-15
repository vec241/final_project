__author__ = 'fnd212'
__reviewer__ = 'sb5518'

class QuitProgram(Exception):
	pass

class FatalError(Exception):
	def __init__(self, message):
		self.message = message
