import unittest
from unittest import TestCase
import geometry_utils as gu

class Test_geometry(TestCase):

	def setUp(self):
		#Correct input list of list or list of tuples (list of two elements)
		self.valid_input = [zip([41.4566,41.4565,41.4564],[-87.231,-87.230,-87.229]), zip((1,2,3),(2,3,4))]

		#Incorrect value 1, not list with 2 elements or another type
		self.invalid_input = [[1,2,3], 2,'a', ]

		#Incorrect value 2, list with more than 2 elements
		self.invalid_input2 = [zip([1,2,3],[2,3,4], [1,1,1])]

		#useful references 
		self.reference1 = (41.4567, -87.2324)
		self.reference2 = (41.478, -87.2899)

	def test_exceptions_return_points_in_polygon(self):
		#If the input s correct it must create a list
		for i in range(len(self.valid_input)):
			assert isinstance(gu.return_points_in_polygon(zip(self.reference1, self.reference2),self.valid_input[i]), list)

		#If it is incorrect(type1)it must raise an exception
		for i in range(len(self.invalid_input)):
			self.assertRaises(TypeError, gu.return_points_in_polygon, self.reference1, self.invalid_input[i])

		#Similarly for type 2			
		for i in range(len(self.invalid_input2)):
			self.assertRaises(TypeError, gu.return_points_in_polygon, self.reference1, self.invalid_input2[i])

	def text_output_return_points_in_polygon(self):
		#Validates that it retunrs a list
		assert isinstance(gu.return_points_in_polygon(self.reference1,valid_input[0]), list) 


	def test_equal_distance_between_points(self):

		#Distance should be the same, no matter the order the points are inputted
		distance1 = gu.calculate_distance_between_points(self.reference1[0], self.reference1[1], self.reference2[0],self.reference2[1])
		distance2 = gu.calculate_distance_between_points(self.reference2[0], self.reference2[1], self.reference1[0],self.reference1[1])

		self.assertEqual(distance2, distance1)
	

if __name__ == '__main__':
	unittest.main()
