import unittest
from unittest import TestCase
import pandas as pd 
import numpy as np
import math
import operator
import sys
import re
import warnings
from general_function.user_defined_exceptions import *
import general_function.general_functions as gf
import general_function.option_functions as op
from prediction_recommendation.frequency_statistics import FrequencyStatistics
import prediction_recommendation.prediction_and_recommendation as pr 
import station_plot.mapplot as sm
import station_plot.freq_station as fs
import plot_tool.plotting_tool as vs

class TestDataVisualization(TestCase):
    """
    This class will test the functions and methods of classes for options 1 and 2.
    """
    
    def setUp(self):
        # load data
        try:
            self.data = pd.read_csv('data/Citibike_final.csv')
        except IOError:
            print "can not find the data file, Goodbye"
            sys.exit()
        data_month = gf.data_extract(self.data, 2014, 1, 2014, 1)
        loc_data = fs.station_info(data_month, 2014, 1)
        self.map_plot_obj = sm.MapPlot(loc_data,1,2014)
        
    # test option 2   
    def test_get_color(self):
        '''the method will test the get_red_color function MapPlot class in the mapplot module '''
        self.assertEqual(self.map_plot_obj.get_red_color(20,10,15),0.5)
        self.assertEqual(self.map_plot_obj.get_blue_color(30,10,25),0.25)

    # test plotting_tool
    def test_plottingTool_1(self):
        data_month = gf.data_extract(self.data, 2014, 1, 2014, 1)
        month_data = vs.visualizationTool(data_month, 2014, 1)
        self.assertEqual(month_data.year, 2014)
        self.assertEqual(month_data.month, 1)

    def test_plottingTool_2(self):      
        data_month = gf.data_extract(self.data, 2015, 3, 2015, 3)
        month_data = vs.visualizationTool(data_month, 2015, 3)
        self.assertEqual(month_data.year, 2015)
        self.assertEqual(month_data.month, 3)

    # test station frequency
    def test_freq_stat_1(self):
        # case 1
        data_month1 = gf.data_extract(self.data, 2014, 1, 2014, 1)
        loc_data1 = fs.station_info(data_month1, 2014, 1)
        stat_list1 = fs.high_freq_station(loc_data1, 2)
        self.assertEqual(set(stat_list1), set(['Pershing Square N', '8 Ave & W 31 St']))
        # case 2
        data_month2 = gf.data_extract(self.data, 2015, 1, 2015, 1)
        loc_data2 = fs.station_info(data_month2, 2015, 1)
        stat_list2 = fs.high_freq_station(loc_data2, 3)
        self.assertEqual(set(stat_list2), set(['8 Ave & W 31 St', 'Lafayette St & E 8 St', 'E 43 St & Vanderbilt Ave']))
        # case 3
        data_month3 = gf.data_extract(self.data, 2013, 12, 2013, 12)
        loc_data3 = fs.station_info(data_month3, 2013, 12)
        stat_list3 = fs.high_freq_station(loc_data3, 5)
        self.assertEqual(set(stat_list3), set(['8 Ave & W 31 St', 'Pershing Square N', 'W 21 St & 6 Ave', 'E 17 St & Broadway', '8 Ave & W 33 St']))

            

class TestFrequencyStatistics(unittest.TestCase):
    """
    This class will test the functions and methods of classes for option 3.
    """

    def setUp(self):

        self.data = pd.DataFrame(np.array([[164, 2013, 7 ,1],[388, 2013, 7 ,1],[293, 2013, 7 ,1],[531, 2013, 7 ,1],[382, 2013, 7 ,1]]),
            columns = ['start station id', 'startyear', 'startmonth', 'startday'])
        self.dictionary = { 164: ['E 47 St & 2 Ave', 40.75323098, -73.97032517], 293: ['Lafayette St & E 8 St', 40.73028666, -73.9907647], 
            382: ['University Pl & E 14 St', 40.73492695, -73.99200509], 388: ['W 26 St & 10 Ave', 40.749717753, -74.002950346],
            531: ['Forsyth St & Broome St', 40.71893904, -73.99266288]}

    def test_right_input(self):

        freq_stat = FrequencyStatistics(self.data, self.dictionary, '164', '7', '1')
        self.assertEqual(1, freq_stat._usage_station_day_given())

    def test_inputstationidformaterror(self):

        self.assertRaises(InputStationidFormatError, lambda: FrequencyStatistics(self.data, self.dictionary, '164error', '7', '1'))

    def test_inputmonthformaterror(self):

        self.assertRaises(InputMonthFormatError, lambda: FrequencyStatistics(self.data, self.dictionary, '164', '7error', '1'))

    def test_inputdayformaterror(self):

        self.assertRaises(InputDayFormatError, lambda: FrequencyStatistics(self.data, self.dictionary, '164', '7', '1error'))

    def test_inputstationidoutrange(self):

        self.assertRaises(InputStationidOutRange, lambda: FrequencyStatistics(self.data, self.dictionary, '165', '7', '1'))

    def test_inputmonthoutrange(self):

        self.assertRaises(InputMonthOutRange, lambda: FrequencyStatistics(self.data, self.dictionary, '164', '13', '1'))

    def test_inputdayoutrange(self):

        self.assertRaises(InputDayOutRange, lambda: FrequencyStatistics(self.data, self.dictionary, '164', '2', '29'))

if __name__ == '__main__':
    unittest.main()
