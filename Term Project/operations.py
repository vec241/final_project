import pandas as pd
import numpy as np
import datetime as dt
from sklearn.linear_model import LinearRegression
from dataclean import *
from feature_selection import *
from visualization import *

def load_data():
    '''
    Supplementary function for main program.
    '''
    train = pd.read_csv('train.csv', header=0, low_memory=False)  #read data
    store = pd.read_csv('store.csv', header=0, index_col='Store') #read data
    test = pd.read_csv('test.csv', header=0) #read data

    print 'Loading data... Please be patient.'
    data = Data(train, store, test)

    return data



def operate_data(grand, storeId, data):
    '''
    Supplementary function for main program.
    '''
    predictors = select_vars(grand)

    X = grand[predictors]
    Y = grand['Sales']

    model = LinearRegression()
    model.fit(X, Y)

    test_fill = get_test(storeId, data, model, predictors)
    generate_plot(test_fill)

    return test_fill