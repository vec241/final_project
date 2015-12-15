

import unittest
from unittest import TestCase
import indicators_utils as iu
import databases_utils as du
import pandas as pd
from indicators_utils import ZeroAreaPolygon

class Test_indicators(TestCase):

	def setUp(self):
		self.boundaries = du.get_polygon(11)
		self.data = pd.read_csv('./tests/csv_for_test.csv')

	def test_effectiveness_police(self):
		data1 = self.data.drop('Arrest',1)
		self.assertRaises(ValueError,iu.effectiveness_police,data1)

	def test_get_density(self):
		self.assertTrue(iu.get_density(self.boundaries, len(self.data)))

if __name__ == '__main__':
    unittest.main()

