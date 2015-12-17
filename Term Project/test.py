import unittest
from unittest import TestCase
from dataclean import *
from feature_selection import *
from visualization import *
import pandas as pd
from operations import *
import os


class test(unittest.TestCase):

    def setUp(self):
        pass

    # test two invalid inputs 1200 and 0
    def test_input_1200(self): 
        self.assertRaises(KeyError, userId = 1200)

    def test_input_0(self):
        self.assertRaises(KeyError, userId = 0)
    #test the input error
    def test_input_abc(self):
        self.assertRaises(KeyError, userId = 'abc')


    #test the file formed by program is in correct format
    def test_plot(self):
        data = load_data()
        grand = pd.read_csv('grand_data.csv', header=0) 
        storeId = 118
        operate_data(grand, storeId, data)
        self.assertTrue(os.path.isfile('prediction_sales_of_Store_{}.png'.format(storeId)))

if __name__ == '__main__':
    unittest.main()