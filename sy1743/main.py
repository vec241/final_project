import pandas as pd
import numpy as np
import math
import operator
import sys
import re 
import warnings
import station_plot.mapplot #plot map
import station_plot.freq_station as fs
import general_function.general_functions as gf
import general_function.option_functions as op
from general_function.user_defined_exceptions import *


# DS-GA 1007 Final Project
# Main program
# Author: Sida Ye, Junchao Zheng, Muhe Xie

"""
This program has three options:
Option 1: generate four graphs with two pie plots and two bar plots: gender distribution, user type distribution, daily usage and daily miles
Option 2: The station frequency visualization part will print the name of top 5 high frequency stations and generate 3 plots automatically (close one to see the next plot).
Option 3: Recommendation and predication. Get information of usage of the station on that particular date on historical date and get recommendation on the station.
Get two alternative stations nearby which meet with the criterion: I. within 15-minute walk, II. predicted to be recommended.
"""

def main():
    
    data, station_dictionary = op.get_data_and_dictionary_main_function()
    
    while True:
        try:
            print 'Main Menu:'
            print '=============================================================\n'
            print 'You have several options. Enter 1 or 2 or 3 to choose your option, enter quit to exit the program'
            print '\n Option 1: Monthly Data Visualization'
            print '\n Option 2: Station Frequency Visualization'
            print '\n Option 3: Prediction and Recommendation'
            print '\n==========================================================='
            
            main_option= raw_input('\nPlease enter your option: ')
            if not re.match('([123]|quit)$',main_option):
                raise OptionInputError
            else:
                pass

                if main_option == 'quit':
                    print '\nThanks, bye!'
                    sys.exit()

                elif main_option == '1':
                    op.month_analysis_main_function(data)

                elif main_option == '2':
                    op.station_freq_visualization_main_function(data)

                else:  
                    op.recommendation_main_function(data, station_dictionary)

        except OptionInputError:
            print 'Invalid input'

if __name__ == '__main__':
    try:    
        main()

    except KeyboardInterrupt:
        print 'the program has been interrupted by KeyboardInterrupt, thanks for trying,Goodbye'
    except EOFError:
        print 'the program has been interrupted by EOFERROR, thanks for trying, Goodbye'
    except TypeError:
        print 'the program has been interrupted by TypeError, thanks for trying, Goodbye'
    except OverflowError:
        print 'the program has been interrupted by OverflowError, thanks for trying, Goodbye'