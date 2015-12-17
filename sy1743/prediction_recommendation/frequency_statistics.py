import math
import pandas as pd
import numpy as np
from collections import Counter
import general_function.general_functions as gf
from general_function.user_defined_exceptions import *

# DS-GA 1007 Final Project
# Station frequency statistics on historical data
# Author: Junchao Zheng

class FrequencyStatistics():
    """
    The FrequencyStatistics class generates several attributes including:
    Station ID, the month and day of a particular date; predifined data and station dictionary.
    In the class we handle exceptions and raise certain user-defined exceptions when invalid input is given.
    And three functions under the class to calculate statistics of the usage of the given station on the given date, the usage of the given station over all dates and the usage of all stations over all dates respectively.
    Statistics of the usage includes median and percentile at 0.8.
    """

    def __init__(self, data, station_dictionary, station_id, month, day):

        # Lists of month with 31 or 30 days
        MONTH_31DAYS = [1, 3, 5, 7, 8, 10, 12]  
        MONTH_30DAYS = [4, 6, 9, 11]
        MONTH_FEB = [2]

        # Input dataset cover all historical data.
        self.data = data
        self.station_dictionary = station_dictionary

        # Check input for station_id, month and day has right format, else raise error.
        if gf.RepresentsInt(station_id):
            pass
        else:
            raise InputStationidFormatError

        if gf.RepresentsInt(month):
            pass
        else:
            raise InputMonthFormatError

        if gf.RepresentsInt(day):
            pass
        else:
            raise InputDayFormatError

        # Check input for station_id within right range, else raise error.
        if int(station_id) not in station_dictionary.keys():
            raise InputStationidOutRange
        else:
            self.station_id = int(station_id)  # self.station_id has int format.

        # Check input for month, day within right range, else raise error respectively.
        # self.month and self.day has int format.
        if int(month) in MONTH_31DAYS:  # For month which has 31 days.
            if int(day) < 1 or int(day) > 31:
                raise InputDayOutRange
            else:
                self.day = int(day)
                self.month = int(month)
        elif int(month) in MONTH_30DAYS:  # For month which has 30 days. 
            if int(day) < 1 or int(day) > 30:
                raise InputDayOutRange
            else:
                self.day = int(day)
                self.month = int(month)
        elif int(month) in MONTH_FEB:
            if int(day) < 1 or int(day) > 28:
                raise InputDayOutRange
            else:
                self.day = int(day)
                self.month = int(month)
        else:
            raise InputMonthOutRange

    def _usage_station_allyear(self):
        """
        Function to generate statistics of usage of all stations over all dates.
        """

        freq_station_allyear = Counter(self.data['start station id'])
        freq_allyear_values = np.array(freq_station_allyear.values())
        number_of_day = len(self.data['startdate'].unique())
        freq_allyear_median = np.median(freq_allyear_values)/number_of_day
        freq_allyear_percentile = np.percentile(freq_allyear_values, 80)/number_of_day
        return freq_allyear_median, freq_allyear_percentile

    def _usage_station_day_given(self):
        """ 
        Function to generate statistics of usage of given station on given date.
        """

        data_station_given = self.data[self.data['start station id'] == self.station_id]
        data_station_month = data_station_given[data_station_given['startmonth'] == self.month]
        data_station_day = data_station_month[data_station_month['startday'] == self.day]
        freq_station_weight = data_station_day.shape[0]/(max(1,len(data_station_day['startyear'].unique())))
        return freq_station_weight

    def _usage_station_given(self):
        """
        Function to generate statistics of usage of given station over all dates.
        """

        data_station_given = self.data[self.data['start station id'] == self.station_id]
        freq_station_given = Counter(data_station_given['startdate'])
        freq_station_median = np.median(np.array(freq_station_given.values()))
        freq_station_percentile = np.percentile(np.array(freq_station_given.values()), 80)
        return freq_station_median, freq_station_percentile
        
