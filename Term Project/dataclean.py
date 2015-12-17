import pandas as pd
import numpy as np
import datetime as dt

class Data(object):

    def __init__(self, train, store, test):
        self.history = clean_history(train)
        self.store = clean_store(store)
        self.test = clean_test(test)
        
def clean_store(store):
    '''
    1. Keeps only the columns we need. 
    2. Fills the NANs in the CompetitionDistance with the mean of other values in this column.
    3. Transfers lowercase into uppercase.
    '''
    store = store[['StoreType', 'Assortment', 'CompetitionDistance']].fillna(np.mean(store['CompetitionDistance']))
    store.Assortment = store.Assortment.apply(lambda x: x.upper())
    store.StoreType = store.StoreType.apply(lambda x: x.upper())
    return store

def clean_history(data):  
    '''
    1. Parses the date column - originally in str type - into month column.
    2. Drops NaNs and the Open and Customers columns, since we don't need them.
    3. Works exclusively for the history data set.
    '''
    data['Date']=pd.to_datetime(data['Date'])   #parse string 'Date' column to dtype 'timestamp'
    data['Month']=np.nan   
    data['Month'] = data['Date'].apply(lambda x: x.month) #fill the empty 'Month' column with months
    data['Month'] = data['Month'].replace([1,2,3,4,5,6,7,8,9,10,11,12], ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    data['DayOfWeek'] = data['DayOfWeek'].replace([1,2,3,4,5,6,7], ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun'])
    data['StateHoliday'] = data['StateHoliday'].replace(['0', 'a', 'b', 'c'], ['None', 'Public', 'Easter', 'Xmas'])
    data = data[data.Open == 1]
    data = data.drop(['Open','Customers'], axis=1)
    data = data.dropna()
    data = data.set_index(np.arange(data.shape[0]))
    return data


def clean_test(data):  
    '''
    1. Parses the Date column - originally in str type - into month column;
    2. Drops NaNs and the Open and Id columns from the test data set, since we don't need it.
    3. Works exclusively for the test data set.
    '''
    data['Date']=pd.to_datetime(data['Date'])   #parse string 'Date' column to dtype 'timestamp'
    data['Month']=np.nan   
    data['Month'] = data['Date'].apply(lambda x: x.month)
    data.Month = data.Month.replace([1,2,3,4,5,6,7,8,9,10,11,12], ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    data['DayOfWeek'] = data['DayOfWeek'].replace([1,2,3,4,5,6,7], ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun'])
    data = data.drop(['Open', 'Id'], axis=1)
    data = data.dropna()
    data = data.replace(['0', 'a'], [0, 1])
    data = data.set_index(np.arange(data.shape[0]))
    return data

class CleanData(object): 
    def __init__(self, data, storeID, day):
        self.data = data
        self.history_total = data.history
        self.store = data.store
        self.test_total = data.test
        self.storeID = storeID
        self.day = day
        self.history = CleanData.clean_and_merge_history(self)
        self.test = CleanData.clean_and_merge_test(self)
        self.history = self.history.drop(['StoreType', 'DayOfWeek', 'Assortment', 'Month', 'StateHoliday'], axis=1)
        self.test = self.test.drop(['StoreType', 'DayOfWeek', 'Assortment', 'Month', 'StateHoliday'], axis=1)
        self.history_features = self.history.drop(['Sales'], axis=1)
        self.history_target = self.history.Sales
        self.test_features = self.test.drop(['Sales'], axis=1)
        self.test_target = self.test.Sales
        
    def clean_and_merge_history(self):
        history_before_merge = separate_store(self.history_total, self.storeID)
        history_merged = merge_data(history_before_merge, self.store, self.storeID)
        history = add_past_sales_history(history_merged, self.day)
        history = create_dummy(history, history, self.store)
        return history
    
    def clean_and_merge_test(self):
        test_before_merge = separate_store(self.test_total, self.storeID)
        test_merged = merge_data(test_before_merge, self.store, self.storeID)
        test = add_past_sales_test(test_merged, self.day)
        test = create_dummy(test, self.history, self.store)
        return test
    
def separate_store(data, storeID):  
    '''
    This function extracts a DataFrame of a given store.
    '''
    data = data.loc[data.Store==storeID]
    data = data.set_index(np.arange(data.shape[0])) #reset the index for convenience
    return data


def merge_data(data, store, StoreID):  
    '''
    This function merges DataFrame of a given store with store.csv to include supplementary data.
    '''
    for column in store.columns: 
            data[column] = store.loc[StoreID, column]
    return data
    
    
def add_past_sales_history(data, days):  
    '''
    This function adds sales from the past as columns. 
    The user can input the desired number of days he/she wants to go back.
    The function works exclusively for the history data set.
    '''
    data = data.dropna()
    for day in np.arange(days):
        col_name = 'Sale' + str(day+1) + 'DaysAgo'
        data[col_name] = np.nan
        for i in np.arange(data.shape[0]-days):
            index_past = i + day
            data.loc[i, col_name] = data.loc[index_past+1, 'Sales'] 
    data = data.drop(data.index[np.arange(-days, 0)])
    return data

def create_dummy(data, history, store):
    '''
    This functions generates dummy variables for the four nominal variables: StoreType, DayOfWeek, Month, Assortment
    '''
    for level in ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']:
        col_name = 'DayOfWeek' + '_' + level
        data[col_name] = (data['DayOfWeek']==level)
        data[col_name] = data[col_name].astype(int)
    for level in ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
        col_name = 'Month' + '_' + level
        data[col_name] = (data['Month']==level)
        data[col_name] = data[col_name].astype(int)
    for column in ['StoreType', 'Assortment']:
        for level in store[column].unique():
            col_name = column + '_' + level
            data[col_name] = (data[column]==level)
            data[col_name] = data[col_name].astype(int)
    for level in ['None', 'Public', 'Easter', 'Xmas']:
        col_name = 'StateHoliday' + '_' + level
        data[col_name] = (history['StateHoliday']==level)
        data[col_name] = data[col_name].astype(int)
    return data


def add_past_sales_test(data, days):  
    '''
    This function adds sales from the past as columns. 
    The user can input the desired number of days he/she wants to go back.
    This function works exclusively for the test data set.
    '''
    data = data.dropna()
    data['Sales'] = np.nan
    for day in np.arange(days):
        col_name = 'Sale' + str(day+1) + 'DaysAgo'
        data[col_name] = np.nan
    data.Sales = np.nan
    return data

def grand_merge(data):
    '''
    Merge back cleaned and engineered dataframes from all stores.
    '''
    total = CleanData(data, 1).history
    for i in np.arange(1, data.history['Store'].unique().shape[0]):
        print ('Merging #' + str(i) + ' ......')
        each = CleanData(data, i+1).history
        total = pd.concat([total, each])
    return total

