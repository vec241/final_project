#__author__ = 'lqo202'
#__reviewer_ = 'fdn212'

import unittest
from unittest import TestCase
import Projections


class Test_Projections(TestCase):
    def test_definition(self):
        #Correct input list of list or list of tuples (list of two elements)
        valid_input = [zip([1,2,3],[2,3,4]), zip((1,2,3),(2,3,4))]
        #Incorrect value 1, not list with 2 elements or another type
        invalid_input = [[1,2,3], 2,'a', ]
        #Incorrect value 2, list with more than 2 elements
        invalid_input2 = [zip([1,2,3],[2,3,4], [1,1,1])]

        for i in range(len(valid_input)):
            self.assertTrue(Projections.PolygonProjection(valid_input[i]))

        for i in range(len(invalid_input)):
            self.assertRaises(TypeError, Projections.PolygonProjection, invalid_input[i])

        for i in range(len(invalid_input2)):
            self.assertRaises(ValueError, Projections.PolygonProjection, invalid_input2[i])

if __name__ == '__main__':
    unittest.main()

