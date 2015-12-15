__author__ = 'fnd212'
__reviewer__ = 'sb5518'

"""
This module contains a set of functions meant to interact with user and request input:

Methods:

- display_welcome_screen()
- print_indexed_items(options)
- get_number_from_user()
- get_timeframe_from_user(max_year, min_year)
- get_options_from_user(options, multiple)
- yesno_question(question)

"""
from defined_exceptions import *
from collections import Iterable
import os
import time


def display_welcome_screen(): 
    print('****************************************************')
    print('Welcome! This is an interactive tool to provide and' + '\n'
    'visualize insights about criminality in the city of Chicago' + '\n'
    'Please be patient while we load the data!')
    print('****************************************************')
    time.sleep(2)


def computing_statistics_message():
    os.system('clear')
    print('Computing statistics ... ')
    print ('\n')

def print_indexed_items(options):
    """
    Receives a dictionary of number and name of the options
    and prints it.

    :param options
    """
    os.system('clear')

    if not isinstance(options,dict):
        if not (isinstance(options,Iterable)):
            raise TypeError('Argument must be an iterable object')
        options = { i+1:option for i,option in enumerate(options)}

    for item in options.items():
        print('[{}]: {}'.format(item[0],item[1]))

def get_number_from_user():
    """
    Asks the user for a number, raises QuitProgram if Q is pressed and raises an
    exception if needed that has to be hhandled by the caller.

    :return num
    """
    while 1:
        try:
            num = raw_input()
        except EOFError:
            continue

        if num == 'Q':
            raise QuitProgram
        try:
            num = int(num)
        except ValueError:
            raise
        return num

def get_timeframe_from_user(max_year, min_year):
    """
    Gets a timeframe from user input and returns start_year, stop_year

    :param max_year, min_year
    :return start_year, stop_year
    """

    os.system('clear')
    start_year = 0

    # Get a number representing a starting year from User.
    while (start_year < min_year) or (start_year > max_year):
        print('Please enter a year to start the analysis (between {} and {}) or [Q]uit: '.format(int(min_year),int(max_year)))
        try:
            start_year = get_number_from_user()
        except (ValueError, EOFError):
            pass
        os.system('clear')            

    os.system('clear')
    stop_year = 0

    # Get a number representing a ending year from User.
    while (stop_year < start_year) or (stop_year > max_year):
        print('Please enter a year to stop the analysis (between {} and {}) or [Q]uit: '.format(start_year,int(max_year)))
        try:
            stop_year = get_number_from_user()
        except (ValueError, EOFError):
            pass
        os.system('clear')  

        

    return start_year, stop_year



def get_options_from_user(options, multiple):
    """
    Receives the possible crimes in an iterable.
    Ask the user to select the crimes of interest
    and returns a list of them.

    :param options, multiple
    :return options_selected
    """
    # Maybe this can be generalized to be a selector of options.

    options_indexed = { i+1:option for i, option in enumerate(options)}

    if multiple:
        options_indexed[0] = 'All'
        options_indexed[-1] = 'Stop adding'

    options_selected = []

    while 1:

        print_indexed_items(options_indexed)
        print('Please select option of interest')
        try:
            option_to_add = get_number_from_user()
        except (ValueError, EOFError):
            option_to_add = None
            pass

        os.system('clear')

        if option_to_add in options_indexed.keys():

            if option_to_add == 0:
                options_selected = options
                break

            elif option_to_add == -1:
             if options_selected:
                break
             else:
                print('Please add at least one option or [Q]uit')
                continue

            if not multiple:
                return options_indexed[option_to_add]
            options_selected.append(options_indexed[option_to_add])
            options_indexed.pop(option_to_add)

        else:
            print ('Not a valid option, please try again or [Q]uit')
            print_indexed_items(options_indexed)
            continue

    return options_selected

def yesno_question(question):
    """
    Receives a Yes/No question and  returns True if user answers 'Yes', or False if user answers 'No'

    :param question
    :return boolean
    """

    print question,' [Y]es or [N]o'

    while 1:
        try:
            answer = raw_input()
            os.system('clear')
        except EOFError:
            #Ignore and ask again
            pass

        if answer == 'Y':
            return True
        if answer == 'N':
            return False

        print('Invalid answer.')
        print question,', [Y]es or [N]o'

