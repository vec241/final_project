__author__ = 'luisa'

import unittest
from unittest import TestCase
from  statistics import  AddressStatistics
import  pandas as pd
from addressClass import Address
from statistics import CrimesDataFrame
from statistics import MalformedCrimesDataFrame
from indicators_utils import ZeroAreaPolygon

class TestAddressStatistics(TestCase):
    def setUp(self):
        self.good_address = Address('4334 W Washington Blv')
        self.data = pd.read_csv('./tests/csv_for_test.csv')

    def test_definition(self):
        reference = (41.917564,-87.753396 )

        #testing input addresses
        assert  isinstance(self.good_address, Address)

        bad_address =  '4334 W Washington Blv'
        self.assertRaises(TypeError, AddressStatistics, bad_address, self.data)

        #Testing columns exist
        for key in ['Year', 'Month', 'Arrest', 'Latitude', 'Longitude']:
            self.data.drop(key, 1, inplace = True)
            self.assertRaises(ValueError, AddressStatistics, self.good_address, self.data)

    def test_get_circle_boundaries(self):
        obj = AddressStatistics(self.good_address,self.data)._get_circle_boundaries()
        assert  isinstance(obj, list)
        self.assertGreaterEqual(len(obj),40)

    def test_get_data_crime_circle(self):
        obj = AddressStatistics(self.good_address,self.data)
        data = pd.DataFrame()
        self.assertRaises(KeyError, obj._get_data_crime_circle,data,)

    def test_generate_db_month_district_indicator(self):
        obj = AddressStatistics(self.good_address,self.data)

        #Valid indicators
        valid_indicators = ['density', 'effect', 'effectsq']

        for ind in valid_indicators:
            assert isinstance(obj._generate_db_month_district_indicator(self.data,ind),pd.Series)

        #Invalid indicators        
        invalid_indicators = ['density_per', 'effectiviv', 'effect_sq']

        for ind in invalid_indicators:
            self.assertRaises(ValueError, obj._generate_db_month_district_indicator, self.data,ind)


class TestCrimesDataFrame(TestCase):
    def setUp(self):
        self.data = pd.read_csv('./tests/csv_for_test.csv')

    def test_definition(self):
        datadrop = self.data.copy()

        #Testing columns exist
        for key in ['Year', 'Month', 'Arrest', 'Latitude', 'Longitude']:
            datadrop.drop(key, 1, inplace = True)
            self.assertRaises(ValueError, CrimesDataFrame,datadrop)

        #Testing creates a dataframe instance
        assert isinstance(CrimesDataFrame(self.data), pd.DataFrame)

        #Testing constructor
        assert isinstance(CrimesDataFrame(self.data[self.data['Year']==2014]), CrimesDataFrame)

    def test_crime_density_by_district(self):
        data1=self.data
        data1[data1['District']==1] == 21
        obj = CrimesDataFrame(data1)        
        obj.crime_density_by_district()



if __name__ == '__main__':
    unittest.main()