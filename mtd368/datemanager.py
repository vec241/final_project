"""ADD COMMENTS"""

#author: Matthew Dunn
#netID: mtd368
#date: 12/12/2015

import datetime
import calendar
from errorhandler import *

def datemanager(inputString):
    validatedDate = validformatchecker(inputString)
    return dateinfuturechecker(validatedDate)

def validformatchecker(inputString):
    userinputskidate = datetime.datetime.strptime(inputString, '%Y-%m-%d')
    return userinputskidate

def dateinfuturechecker(validatedDate):
    now = datetime.datetime.now()
    if validatedDate > now:
        return validatedDate
    raise dateNotinFuture

def datesrangenerator(validatedDate):
    listofdayperiods = [-15,-9,-8,-1,0,6,7,13,14,20]
    weekperiods = []
    for i in listofdayperiods:
        datedelta = datetime.timedelta(days=i)
        changeddate = datedelta + validatedDate
        weekperiods.append(changeddate)
    return weekgrouper(weekperiods)

def weekgrouper (weekperiods):      # takes list of integers and groups them into week periods.
    it = iter(weekperiods)
    finalgroupingofskidates = []
    for x in it:
        temp = [x, next(it)]
        finalgroupingofskidates.append(temp)
    return finalgroupingofskidates

def numberOfDaysinStartMonth(startofweek):
    startofweekyear, startofweekmonth = startofweek.year, startofweek.month
    startMonthLastDay = calendar.monthrange(startofweekyear,startofweekmonth)[1]    # calculates the number of days in month for given data.
    numberofdaysinstartmonth = startMonthLastDay - startofweek.day                  # calculates the number of days until end of month from given date
    return numberofdaysinstartmonth, startMonthLastDay
