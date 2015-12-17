import math
import pandas as pd
import numpy as np
from collections import Counter
from frequency_statistics import FrequencyStatistics

# DS-GA 1007 Final Project
# Station frequency prediction and recommendation on historical data
# Author: Junchao Zheng

def prediction_function(data, station_dictionary, station_id, month, day):

    """
    The function calls the FrequencyStatistics class taking the arguments and then compare the usage of the station for the given date to 1. the average usage of the station over all dates 2. the average usage of all stations over all dates.
    If usage of the station of the given date is above 80 percent of the 1 or 2 values, then we suggest it is busy at that time.
    If usage of the station of the given date is below median of the 1 or 2 values, then we suggest it is available at that time.
    Else we suggest it is possible that the station is available.
    Input: 
    station ID, the month and day of the particular date the user want to explore; predefined dataset and station_dictionary can be left blank.
    Output:
    a list containing a value from {-1, 0, 1} represents not recommend/ mild/ recommend as well as the usage of the station on the given date.
    """
    
    new_instance = FrequencyStatistics(data, station_dictionary, station_id, month, day)  # Call the class to get class attributes
    usage_given = new_instance._usage_station_day_given()  # Compute the average usage of the station on the given day
    usage_allyear_median, usage_allyear_80 = new_instance._usage_station_allyear()  # Compute the average usage of all stations over all days.
    usage_station_median, usage_station_80 = new_instance._usage_station_given()  # Compute the average usage of the station over all days.
    if usage_given > usage_allyear_80 or usage_given > usage_station_80:
        return [-1, usage_given]
    elif usage_given < usage_allyear_median or usage_given < usage_station_median:
        return [1, usage_given]
    else:
        return [0, usage_given]

def prediction_statement(argument):

    """
    The function is a help function to prediction_function, taking output from prediction_function then output strings to users.
    Input: 
    return from prediction_function.
    Output:
    two strings to users include the usage of the station on the given date and the recommendation.
    """

    if argument[0] == -1:
        print 'The usage is %d' % argument[1]
        print 'Not recommended. The station is quite busy at that moment.'
    elif argument[0] == 1:
        print 'The usage is %d' % argument[1]
        print 'Recommended. The station is OK at that moment.'
    elif argument[0] == 0:
        print 'The usage is %d' % argument[1]
        print 'It is possible you can try... I mean worth a try...'

def station_distance(station_id, station_dictionary):
    """
    The function caculates the distance from one given station to all stations.
    Input:
    station ID; predifined station_dictionary can be left blank.
    Output:
    A list of l2 norm distance from one given station to all stations.
    """

    distance_l2norm = []
    for station in station_dictionary.keys():
        distance_l2norm.append(math.sqrt(math.pow(station_dictionary[station][1]-station_dictionary[int(station_id)][1], 2) + math.pow(station_dictionary[station][2]-station_dictionary[int(station_id)][2], 2)))
    return distance_l2norm



def station_nearest_2(data, station_dictionary, station_id, month, day):
    """
    The function finds the 5 nearest station and use recommend function to determine whether it is available at that given date.
    Input:
    station ID, the month and day of the particular date the user want to explore; predefined dataset and station_dictionary can be left blank.
    Output:
    Print out 5 nearest station and our advice on the particular date.
    """

    distance_limit = 1./111 # set up distance limit, 15 mins walking = 1km, convert to long and lat by dividing 111
    distance = station_distance(int(station_id), station_dictionary)
    distance_sorted = sorted(distance)  # Get a sorted list of distance
    
    print 'available station within 15-minute walk shown below:'
    counts = 0
    for i in range(1, len(distance_sorted)):
        if counts <= 1:
            if distance_sorted[i] <= distance_limit:
                for j in range(len(distance)):
                    if distance_sorted[i] == distance[j]:
                        prediction_result = prediction_function(data, station_dictionary, station_dictionary.keys()[j], month, day)
                        if prediction_result[0] == 1:
                            print '\nthe station name is' + str(station_dictionary.values()[j][0])
                            prediction_statement(prediction_result)
                            counts = counts + 1
                        else:
                            break
                    else: 
                        pass
            else:
                print 'No more station available within 15-minute walk.'
                break
                break
        else:
            break
