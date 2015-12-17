__author__ = 'fnd212'

from unittest import TestCase
import results
import pandas as pd
from statistics import CrimesDataFrame
from addressClass import Address

class test_results(TestCase):

    def setUp(self):
        self.address_wrong = 'asdf'
        self.address = Address('4334 West Washington Blvd')

        self.test_db = pd.DataFrame([[1,2,3,4], [1,2,3,4], [1,2,3,4], [1,2,3,4]], columns = ['Year', 'Month', 'Arrest', 'District'])
        self.test_CrimesDataFrame = CrimesDataFrame(self.test_db)

        self.malformed_addresses_array = [1,2,3,4]
        self.addresses_array = [self.address, self.address]
        self.zero_addresses_array = []
        
    def test_address_analysis_output(self):

        with self.assertRaises(TypeError):
            results.address_analysis_output(self.address_wrong,self.test_CrimesDataFrame)
        with self.assertRaises(TypeError):
            results.address_analysis_output(self.address, self.test_db)
        

    def test_comparative_analysis_output(self):
        
        with self.assertRaises(TypeError):
            results.comparative_analysis_output(self.test_db, self.addresses_array)
        
        with self.assertRaises(TypeError):
            results.comparative_analysis_output(self.test_CrimesDataFrame, self.malformed_addresses_array)   

        with self.assertRaises(TypeError):
            results.comparative_analysis_output(self.test_CrimesDataFrame, 1)   

        with self.assertRaises(ValueError):
            results.comparative_analysis_output(self.test_CrimesDataFrame, self.zero_addresses_array)                       
