'''
Created on Dec 15, 2015

@author: rjw366
'''
import sys
from datetime import date

CUMU_CONSTANT = "cumulative"
YEAR_CONSTANT = "year-by-year"

def explainProgram():
    print()
    print("The program will show you where candidates have been recruited from in the US.")
    print("First you must choose cumulative or year-by-year...")
    print("Then what year to search by...")
    print("If at anytime you'd like to leave the program, enter \"exit\" or \"quit\"")
    print()
    
def getAndValidateType():
    userInput = raw_input("Would you like cumulative or year-by-year results?(Enter any substring, if it's in both then it will default to cumulative)")
    if(CUMU_CONSTANT.find(str(userInput).lower().strip()) != -1):
        return CUMU_CONSTANT
    if(YEAR_CONSTANT.find(str(userInput).lower().strip()) != -1):
        return YEAR_CONSTANT
    if(checkForExit(userInput)):
        sys.exit()
    raise ValueError

def getAndValidateYear():
    userInput = raw_input("What year are you interested in?")
    yearInput = int(userInput)
    if(yearInput < 2005):
        print("The company's only been around since 2005")
    elif(yearInput > date.today().year):
        print("That's in the future.")
    elif(checkForExit(userInput)):
        sys.exit()
    else:
        return yearInput
    raise ValueError

def checkForExit(userInput):
    if(str(userInput).lower().strip() == "exit" or str(userInput).lower().strip() == "quit"):
        return True