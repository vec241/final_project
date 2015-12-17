import statsmodels.formula.api as smf
import re
import numpy as np
import pandas as pd
from dataclean import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def select_vars(grand):
    '''
    This function is for feature selection. 
    The main point is that we run a multiple linear regression with all variables in the structured dataframe, 
    and choose all variables with p-values smaller than 0.05. This function returns a list of chose variables' names.

    '''
    model = 'Sales ~ '
    for string in list(grand.columns):
        if string == list(grand.columns)[-1]:
            model += string
        elif string not in ['Sales', 'Date', 'Store']:
            model = model + string + ' +'
    lm = smf.ols(formula=model, data=grand).fit()
    predictors = list(lm.pvalues.keys()[lm.pvalues<0.05])
    predictors.pop(0)
    return predictors

def get_test(storeId, data, model, predictors):
    '''
    1. Use the column list returned from feature selection to reduce the dimensions of both history and test dataframes.
    2. Merge the history and test dataframes, and fit the regression model built from the grand data onto the test data.
    '''
    columns = predictors + ['Sales', 'Date', 'Store']
    cd = CleanData(data, storeId, 7)
    history = cd.history[columns]
    test = cd.test[columns]
    columns = list(test.columns)
    days = [int(re.search(r"[0-9]+", x).group()) for x in columns if re.search(r"[0-9]+", x) != None]
    total = pd.concat([test, history])
    total = total.set_index(np.arange(total.shape[0]))
    test_i = test.shape[0]
    for i in xrange(test_i):
        for day in days:
            total.loc[test_i-1-i, 'Sale'+str(day)+'DaysAgo'] = total.loc[test_i-1-i+day, 'Sales']
        total.loc[test_i-1-i, 'Sales'] = model.predict(total.loc[test_i-1-i, predictors])
    total['Date'] = [mdates.date2num(datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S')) for x in total['Date']]
    return total.loc[:test_i-1]