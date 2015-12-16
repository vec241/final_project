'''
Varun D N - vdn207@nyu.edu
'''

'''Contains class definition for the different crimes in the data'''

import custom_exceptions as cexcep

class Crimes:
	'''Class definition'''

	def __init__(self, crimes, years_recorded, crime_full_names):
		'''Constructor'''

		self.crimes = crimes
		self.years_recorded = years_recorded
		self.crime_full_names = crime_full_names

	def get_crimes_list_short(self):
		'''Returns the list of names of crimes recorded in short form'''

		return self.crimes 

	def get_crimes_list_long(self):
		'''Returns the list of crimes recorded in expanded form'''

		return self.crime_full_names.values()

	def get_years_recorded(self):
		'''Returns the list of years when the data was recorded'''

		return self.years_recorded

	def get_full_name(self, crime):
		'''Returns the full name of a crime'''

		if crime in self.crime_full_names.keys():
			return self.crime_full_names[crime]
		else:
			raise cexcep.CrimeNotFoundError("Crime not found in the records")

	def get_crimes_column_names(self):
		'''Returns the names of the columns in the data pertaining to the crimes'''

		return [crime + year for year in self.years_recorded for crime in self.crimes]
