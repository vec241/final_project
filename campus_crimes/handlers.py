'''
Varun D N - vdn207@nyu.edu
'''

'''Contains functions which handle different fuctionalities of the system'''

import crimes
import college as coll
import pandas as pd 
import numpy as np

def data_initialization(path):
	'''Initializes the initial data requirements of the system'''

	try:
		data_frame = pd.read_csv(path)

	except IOError as IOE:
		print str(IOE)

	# Crime types and their specifics
	crimes_list = ['MURD', 'NEG_M', 'FORCIB', 'NONFOR', 'ROBBE', 'AGG_A', 'BURGLA', 'VEHIC', 'ARSON']
	years = ['10', '11', '12']
	crime_full_names = {"MURD":"Murder", "NEG_M":"Negligent Manslaughter", "FORCIB":"Forcible Sex Offense", "NONFOR":"Non Forcible Sex Offense", "ROBBE":"Robbery", "AGG_A":"Aggravated Assault", "BURGLA":"Burglary", "VEHIC":"Motor Vehicle Theft", "ARSON":"Arson"}

	# Renaming columns. Using hierarchical indexing
	actual_columns = data_frame.columns.values.tolist()
	abstract_columns = ['BASIC'] * 8 + ['MURD', 'NEG_M', 'FORCIB', 'NONFOR', 'ROBBE', 'AGG_A', 'BURGLA', 'VEHIC', 'ARSON'] * 3 + ['FILTER'] * 3

	# Resetting the column names as a hierarchy
	hierarchical_column_index = pd.MultiIndex.from_arrays([abstract_columns, actual_columns])	# PANDAS
	data_frame.columns = hierarchical_column_index
	data_frame.columns.names = ['ABSTRACT', 'SPECIFIC']

	crimes_obj = crimes.Crimes(crimes_list, years, crime_full_names)

	return data_frame, crimes_obj


def college_details(dataframe, university_name, branch_name):
	'''Returns the row pertaining to the college and it's branch'''

	return dataframe[(dataframe['BASIC']['INSTNM'] == university_name) & (dataframe['BASIC']['BRANCH'] == branch_name)]


def all_crimes_per_student_over_years(college_obj, crimes_obj, per_student = True, average = False):
	'''
	The college instance represents the college specific tuple. The crimes_obj is the same throughout the program.
	If per_student = False, then the frequencies of crimes will be returned instead of per student.

	If average=True, the average over the 3 years will be computed and returned.

	Returns a dictionary with key=Crime and value=list (3 values) or average (1 value)
	'''

	#college_obj = coll.College(college_instance, crimes_obj)
	all_crimes_frequencies = college_obj.get_all_crimes_frequencies()

	if not per_student:
		return all_crimes_frequencies

	total_students = college_obj.get_total_students()[0] 	# Because, the function is returning a list. Eg: [4567.]

	crime_per_student = {}
	for crime in all_crimes_frequencies.keys():	
		try:
			if average:
				crime_per_student[crime] = all_crimes_frequencies[crime].sum() / total_students 	# Question 2
			else:
				crime_per_student[crime] = all_crimes_frequencies[crime][0] / total_students  	# Question 1

		except ZeroDivisionError as z:
			print str(z)

		except ValueError as v:
			print str(v)

	return crime_per_student


# Question 3
def average_crimes_per_student_by_category(dataframe, category, crimes_obj, overall_average = False):
	'''Returns the rate of crimes per student for every crime for a given category - where category can be thought
	   as ZIP Codes, State, College Sector

	   The output is a dictionary with key = crime and value is a series where indices are the different categories
	   and the values are rate of 'crime' per student in that sector

	   overall_average - set to True if you need the average over the years.)

	'''

	crimes_by_category_dict = {}
	groupby_category_with_aggregation = dataframe.groupby(by=[('BASIC', category)]).aggregate(np.sum)
	total_students = groupby_category_with_aggregation[('BASIC', 'Total')]

	for crime in crimes_obj.get_crimes_list_short():
		if overall_average:
			crimes_by_category_dict[crime] = groupby_category_with_aggregation[crime].div(total_students.ix[0], axis = 'rows').sum(axis=1)
		else:
			crimes_by_category_dict[crime] = groupby_category_with_aggregation[crime].div(total_students.ix[0], axis = 'rows')

	return crimes_by_category_dict

