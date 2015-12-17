import pandas as pd
import numpy as np
import math
import sys
import warnings
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from user_defined_exceptions import *
import general_functions as gf
import station_plot.mapplot as sm 
import station_plot.freq_station as fs
import plot_tool.plotting_tool as vs
import prediction_recommendation.prediction_and_recommendation as pr
from prediction_recommendation.frequency_statistics import FrequencyStatistics

"""
Option functions will be used in main program.
"""


def get_data_and_dictionary_main_function():
    """
    load data and dictionary file into memory.
    """

    print '\n================================================================'
    print 'Initializing...'
    print 'Reading the data(around 2 minutes)...'
    try:   ##minor change 1208
        print 'reading .csv data file...'
        data = pd.read_csv('data/Citibike_final.csv')
        print 'reading .p dictionay file...'
        station_dictionary = gf.get_dictionary('data/station_dictionary.p')
        print 'Initialized!'
        print '===============================================================\n'
    except IOError:
        print 'IOERROR happens when reading the data, please make sure the datafile is downloaded and placed at the current directory.'
        sys.exit()
    except KeyboardInterrupt:
        print 'The program has been interrupted.'

    return data, station_dictionary


def month_analysis_main_function(data):
    """
    This function is going to use in main program, which will generate plots for monthly citibike data.
    """

    while True:
        print '\n**************************************************************'
        print '\nPart 1 Instruction:\n'
        print 'Please enter valid year and month from 2013/7 to 2015/10. Year format: 2015, Month format: 7\n'
        print 'Enter back: return to main meun.'
        print 'Enter quit: exit this program.\n'
        print '*****************************************************************\n'
        year = raw_input('Please enter a year: ')
        if year == 'quit':
            print '\nThanks, bye!'
            sys.exit()
        elif year == 'back':
            break
        month = raw_input('Please enter a month: ')
        if month == 'quit':
            print '\nThanks, bye!'
            sys.exit()
        elif month == 'back':
            break
        if gf.check(year, month):
            year_int = int(year)
            month_int = int(month)
            print 'Please wait.......'
            data_month = gf.data_extract(data, year_int, month_int, year_int, month_int)
            object_plot = vs.visualizationTool(data_month, year_int, month_int)
            print '====> Generating gender distribution pie plot...'
            object_plot.pieplot('gender')
            print '====> Generating usertype distribution pie plot...'
            object_plot.pieplot('usertype')
            print '====> Generating daily usage plot...'
            object_plot.plot_daily_freq(show_mile=False)
            print '====> Generating daily miles plot...'
            object_plot.plot_daily_freq(show_mile=True)
        else:
            print '\nError: Please enter valid year and month!\n'
    return

def station_freq_visualization_main_function(data):
    """
    This function is going to use in main program, which will generate map plots for station frequency.
    """    

    while True:
        try:
            print '\n*****************************************************************'
            print '\nPart 2 Instruction:\n'
            print 'Please enter valid year and month from 2013/7 to 2015/10. Year format: 2015, Month format: 7\n'
            print 'Enter back: return to main meun.'
            print 'Enter quit: exit this program.\n'
            print '*****************************************************************\n'
            year = raw_input('Please enter a year: ')
            if year == 'back':
                break
            if year == 'quit':
                print '\nThanks, bye!'
                sys.exit()
            month = raw_input('Please enter a month: ')
            if month == 'back':
                break
            if month == 'quit':
                print '\nThanks, bye!'
                sys.exit()
            if not gf.check(year,month):
                raise InvalidInputError
            else:
                month = int(month)
                year = int(year)
                top_choice = 5 #shouw top 5 stations
                data_month = gf.data_extract(data, year, month, year, month)
                print '====> Calculating top 5 high frequency station...'
                loc_data = fs.station_info(data_month, year, month)
                print 'Show top 5 high frequency station:\n'
                stat_list = fs.high_freq_station(loc_data, top_choice)
                print stat_list
                map_plot_obj = sm.MapPlot(loc_data,month,year)
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    print '\n====> Generating frequency map...'
                    map_plot_obj.draw_freq_map()
                    print '====> Generating high frequency map...'
                    map_plot_obj.draw_top_k_freq_map(top_choice)
                    print '====> Generating high heat map...'
                    map_plot_obj.draw_heat_map()


        except InvalidInputError:
            print '\nError: The input time is invalid!\n'
    return 

def recommendation_main_function(data, station_dictionary):
    """
    This function is going to use in main program, which will do recommendation and prediction for certain date.
    """

    while True:
        print '\n*****************************************************************'
        print '\nPart 3 Instruction:\n'
        print 'Please enter 1 or 2 to start the prediction or recommendation function:'
        print 'Please enter station ID, month and day of the date to make a prediction.\n'
        print 'Enter back: return to main meun.'
        print 'Enter quit: exit this program.\n'
        print '*****************************************************************\n'
        
        try:
            x = raw_input('\nPlease enter your option: ')

            if x == '1':
                print '\n*****************************************************************'
                print '\nPlease enter station ID, month and day of the date to make a prediction.\n'
                print '*****************************************************************\n'
                try:
                    station_id = raw_input('Please enter a station ID: ')
                    month = raw_input('Please enter a month: ')
                    day = raw_input('Please enter a day: ')
                    prediction_result = pr.prediction_function(data, station_dictionary, station_id, month, day)
                    print '====> Now generate the prediction of the usage of the station...\n'
                    pr.prediction_statement(prediction_result)
                except InputStationidFormatError:
                    print '\nError: The input of station id has wrong format!\n'
                except InputMonthFormatError:
                    print '\nError: The input of month has wrong format!\n'
                except InputDayFormatError:
                    print '\nError: The input of day has wrong format!\n'
                except InputStationidOutRange:
                    print '\nError: The station ID does not exist!\n'
                except InputDayOutRange:
                    print '\nError: The day does not exist!\n'
                except InputMonthOutRange:
                    print '\nError: The month does not exist!\n'

            elif x == '2':
                print '\n*****************************************************************'
                print '\nPlease enter station ID, month and day of the date to make a recommendation.\n'
                print '*****************************************************************\n'
                try:
                    station_id = raw_input('Please enter a station ID: ')
                    month = raw_input('Please enter a month: ')
                    day = raw_input('Please enter a day: ')
                    FrequencyStatistics(data, station_dictionary, station_id, month, day)
                    print '\n====> Now generate the recommendation of nearest 2 available station...\n'
                    pr.station_nearest_2(data, station_dictionary, station_id, month, day)
                except InputStationidFormatError:
                    print '\nError: The input of station id has wrong format!\n'
                except InputMonthFormatError:
                    print '\nError: The input of month has wrong format!\n'
                except InputDayFormatError:
                    print '\nError: The input of day has wrong format!\n'
                except InputStationidOutRange:
                    print '\nError: The station ID does not exist!\n'
                except InputDayOutRange:
                    print '\nError: The day does not exist!\n'
                except InputMonthOutRange:
                    print '\nError: The month does not exist!\n'

            elif str.lower(x) == 'back' or str.lower(x) == 'b':
                break
            elif str.lower(x) == 'quit' or str.lower(x) == 'q':
                print '\nThanks, bye!'
                sys.exit()
            else:
                raise OptionInputError

        except OptionInputError:
           print '\nError: Invalid input!\n'
    return 
