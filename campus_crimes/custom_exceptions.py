'''
Varun D N - vdn207@nyu.edu
'''

'''Custom exceptions for the program'''

class CrimeNotFoundError(Exception):
	'''Invalid crime query is flagged'''
	pass

class WrongFormat(Exception):
	'''Invalid format for the module plottingParameters'''
	pass