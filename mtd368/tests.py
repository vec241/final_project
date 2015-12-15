# test case

"""This runs tests on the program to confirm intended functionality is occur."""

#author: Matthew Dunn
#netID: mtd368
#date: 12/12/2015

import os
import unittest
import datetime
from unittest import TestCase
from dataanalyzer import *
from dataloader import *
from datemanager import *
from intializer import *
from userinputmanager import *

"""test function in dataanalyzer.py"""

class unittestsdataanalyzer(unittest.TestCase):

    def test_dataloader(self):
        loaddata()
        self.assertEqual(True, os.path.isfile('snow.txt'))

    def test_monthlytextweatherdatamunger(self):
        monthlyWeather = monthlytextweatherdatamunger()
        listofcolumnvalues = ['Station', 'Year', 'Month', 'Snow', 'Day01', 'Day02', 'Day03', 'Day04', 'Day05', 'Day06', 'Day07', 'Day08', 'Day09', 'Day10', 'Day11', 'Day12', 'Day13', 'Day14', 'Day15', 'Day16', 'Day17', 'Day18', 'Day19', 'Day20', 'Day21', 'Day22', 'Day23', 'Day24', 'Day25', 'Day26', 'Day27', 'Day28', 'Day29', 'Day30', 'Day31']
        self.assertEqual(listofcolumnvalues, list(monthlyWeather.columns.values))

    def test_staiondatamunger(self):
        stationvalues = staiondatamunger()
        listofcolumnvalues = ['LAT', 'LONG', 'ELEV', 'STATE', 'NAME', 'GSNFLAG', 'HCNFLAG', 'WMOID']
        self.assertEqual(listofcolumnvalues, list(stationvalues.columns.values))

    def test_datemanager(self):
        validateddate = datetime.datetime.strptime('2016-01-16', '%Y-%m-%d')
        daterange = datesrangenerator(validateddate)
        self.assertEqual(5, len(daterange))

    def test_datesrangenerator(self):
        inputdate = '2016-01-16'
        date = datetime.datetime.strptime(inputdate, '%Y-%m-%d')
        daterange = datemanager(inputdate)
        self.assertEqual(date, daterange)


if __name__ == '__main__':
    unittest.main()
