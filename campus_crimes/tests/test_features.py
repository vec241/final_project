'''
Varun D N - vdn207@nyu.edu
'''

'''Test Cases for functionalities of the software'''

from unittest import TestCase
import handlers
import pandas as pd
import os
import college as coll

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), 'oncampuscrime101112_cleaned.csv')

class FunctionalityTests(TestCase):
	'''Defines the test cases'''

	def setUp(self):
		'''Sets up the testing environment'''

		self.valid_file_path = TESTDATA_FILENAME
		self.invalid_file_path = "fake.csv"
		self.dataframe, self.crimes_object = handlers.data_initialization(TESTDATA_FILENAME)
		self.valid_university_name = "University of California-Berkeley"
		self.invalid_university_name = "Joke"
		self.valid_branch_name = "Main Campus"
		self.invalid_branch_name = "Jill"

	def test_data_initialization(self):
		'''All validations of the data initialization function are tested '''

		self.assertRaises(UnboundLocalError, handlers.data_initialization, self.invalid_file_path)	# Should throw an error because the file is not present

		self.data_initialization_return = handlers.data_initialization(self.valid_file_path)	# Valid instantiation
		self.assertEquals(len(self.data_initialization_return), 2)	# 2 parameters are returned through valid instantiation

		self.assertEquals(self.data_initialization_return[0].shape, self.dataframe.shape)
		
	def test_college_details(self):
		''' The function should return either a single row or no rows '''

		self.valid_row = handlers.college_details(self.dataframe, self.valid_university_name, self.valid_branch_name)
		self.invalid_row1 = handlers.college_details(self.dataframe, self.valid_university_name, self.invalid_branch_name)
		self.invalid_row2 = handlers.college_details(self.dataframe, self.invalid_university_name, self.invalid_branch_name)
		self.invalid_row3 = handlers.college_details(self.dataframe, self.invalid_university_name, self.valid_branch_name)
	
		self.assertEquals(self.valid_row.shape[0], 1)
		self.assertEquals(self.invalid_row1.shape[0], 0)
		self.assertEquals(self.invalid_row2.shape[0], 0)
		self.assertEquals(self.invalid_row3.shape[0], 0)

	def test_all_crimes_per_student_over_years(self):
		'''The function tests the valid responses of the crime per student function'''

		self.college_instance = handlers.college_details(self.dataframe, self.valid_university_name, self.valid_branch_name)
		self.college_obj = coll.College(self.college_instance, self.crimes_object)
		
		self.test_data1 = handlers.all_crimes_per_student_over_years(self.college_obj, self.crimes_object, True, False)
		
		self.assertEquals(len(self.test_data1['MURD']), 3)