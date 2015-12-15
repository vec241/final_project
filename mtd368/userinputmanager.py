"""The user input module handles requesting the user's input as needed."""

#author: Matthew Dunn
#netID: mtd368
#date: 12/12/2015

import os
import sys
import re
import datetime
from datemanager import datemanager
from errorhandler import *

def userinput():
    unittype = unittypesetter()
    skidate = skidatesetter()
    deviationpenalty = deviationpenaltyinput()
    return unittype, skidate, deviationpenalty

def skidatesetter():
    while True:
        skidate = raw_input('When do you want to go SHRED the GNAR? Format(YYYY-MM-DD)\n')
        try:
            skidatevalidated = datemanager(skidate)
            if skidatevalidated is not None:
                break
        except ValueError:
            print "Please enter a valid date, using format YYYY-MM-DD.\n"
        except dateNotinFuture:
            print "Date must be in the future, please enter valid date of format YYYY-MM-DD.\n"
    return skidatevalidated

def deviationpenaltyinput():
    while True:
        deviationpenalty = raw_input('How much should we penalize the annual fluxations in average snowfall?\n')
        try:
            deviationpenaltyinteger = int(deviationpenalty)
            if type(deviationpenaltyinteger) is int:
                break
        except ValueError:
            print "Please use a valid integer.\n"
    return deviationpenaltyinteger

def unittypesetter():
    while True:
        unittype = raw_input('What unit system would you like, metric(centimeters) or imperial(inches)? Please enter "cm" or "inch". \n')
        if unittype == "inch" or unittype == "cm":
            break
        print '\nIncorrect input type, please enter either "cm" or "inch". \n'
    return unittype

# def programEnder(input):
#     if input.lower() == 'quit':
#         terminationconfirmation = raw_input("Are you sure you want to quit? (y/n)")
#         if terminationconfirmation.lower() == "yes" or terminationconfirmation.lower() == "y":
#             sys.exit()
#         elif terminationconfirmation.lower() == "no" or terminationconfirmation.lower() == "n":
