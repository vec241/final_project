'''
This is the Unittest for the program
'''
import unittest
from unittest import TestCase
import zip_code_belonging_city as zb
import pandas as pd



class Test(unittest.TestCase):



    def test_input(self):
        
        self.assertRaises(KeyboardInterrupt, zip_code = 'abcdefg')
        self.assertRaises(KeyboardInterrupt, zip_code = 123456)
        
    
    def test_show_belonging(self):
        data=pd.read_csv('sample_data.csv')
        self.data=data
        self.dictionary=zb.create_zip_code_dict(self.data)
        self.assertEqual('BROOKLYN',zb.show_belonging('11237', self.dictionary))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()