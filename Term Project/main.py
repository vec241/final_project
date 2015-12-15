import pandas as pd
import numpy as np
import datetime as dt
from sklearn.linear_model import LinearRegression
from dataclean import *
from feature_selection import *
from visualization import *
import sys
import re
from datetime import datetime
from operations import *
import matplotlib.dates as mdates

'''
DS-GA-1007 Final Project
Author:
Yichen Fan
Li Ke lk1818
Kaiwen Liu


This program prompts the user for a store ID. With the store ID, this main function will predict all sales of this store from Aug.1.2015 to Sep.17.2015.
Next, this program will generate a plot of predicted sales over dates of this store in this period.  
'''

def main():

    data = load_data()


    try:
        runornot = raw_input('We already have a structured and cleaned data for you. Do you want to redo the data-engineering process? Please know that this will take over an hour, and will yield the same result. Please enter Yes or No.\n')
        
        if runornot in ['yes', 'Yes', 'YES','Y', 'True', 'y', 'Ok', 'OK']:
            grand_merge(data)
        elif runornot in ['no', 'NO', 'No', 'N', 'n', 'False']:
            grand = pd.read_csv('grand_data.csv', header=0) 
    except (EOFError, KeyboardInterrupt):
        print 'Thank you for using our program. Please have a wonderful day.'
        sys.exit()

    flag = 1
    while flag:
        while True:
            try:
                storeId = raw_input('Please enter a store ID between 1 and 1115 to generate the prediction of sales for that store: \n')
                if storeId in ['finish', 'Finish', 'quit', 'f', 'q', 'Q', 'F', 'QUIT', 'FINISH']:
                    print 'Thank you for using our program. Please have a wonderful day.'
                    sys.exit()
                elif not re.match(r'^[0-9]+$', storeId):
                    raise TypeError
                else:
                    storeId = int(storeId)
                    if storeId >1115 or storeId < 1 or storeId not in list(data.test['Store'].unique()):
                        raise ValueError
                    break
            except (EOFError, KeyboardInterrupt):
                print 'Thank you for using our program. Please have a wonderful day.'
                sys.exit()
            except TypeError:
                print 'Invalid input. Please make sure your input is an integer.'
                continue
            except ValueError:
                print ('Invalid store ID. Please make sure your input is between 1 and 1115. Some of stores are missing from the test dataset, if you happened to input one of those, please try another number.') 
                continue

        test_fill = operate_data(grand, storeId, data)
        print ('A plot of predicted sales versus dates will be saved.')
        
        while True:
            try:
                monthdate = raw_input('Please enter a date between 08/01-09/17 in the format of mmdd:\nEnter no or finish to look at other stores.\n')
                if monthdate in ['no', 'No', 'Finish', 'finish']:
                    break
                elif not re.match(r'^[0-9]{4}$', monthdate):
                    raise TypeError
                else:
                    date = datetime.strptime(str(int(monthdate) + 20150000), '%Y%m%d')
                    if date < datetime.strptime('20150801', '%Y%m%d') or date > datetime.strptime('20150917', '%Y%m%d'):
                        raise ValueError
                    print ('The desired predicted sales is: %.3f' % (test_fill[test_fill['Date'] == mdates.date2num(date)]['Sales']))
                    break
            
            except TypeError:
                print "Invalid input type. Please follow the given format."
                continue
            except ValueError:
                print 'Date beyond range. Your date should be between 08/01 and 09/17.'
                continue
            
        while True:
            try:
                text = raw_input('Do you want to see another store?(y/n):\n')
                if text in ['yes', 'Yes', 'YES','Y', 'True', 'y', 'Ok', 'OK']:
                    flag = 1
                    break
                elif text in ['no', 'NO', 'No', 'N', 'n', 'False']:
                    flag = 0
                    break
                else:
                    raise ValueError
            except ValueError:
                print 'Noncomprehensive response. Please try again.'
                continue
    print "Thank you for using our program. Please have a wonderful day."
    sys.exit()

    
if __name__ == '__main__':
    main()