import pickle

"""
General functions
"""

def get_dictionary(filename):
	""" 
    The function takes a dictionray.p file as input and returns a dictionary.
    """
	
	dictionary = pickle.load(open(filename, 'rb'))
	return dictionary 


def data_extract(data, startyear, startmonth, endyear, endmonth):
    """
    The function helps to extract data from certain period from whole dataset.
    """
    
    data_by_year_start = data.loc[data['startyear'] == startyear]
    data_by_month_start = data_by_year_start.loc[data_by_year_start['startmonth'] == startmonth]
    startindex = data_by_month_start.index[0]
    
    data_by_year_end = data.loc[data['startyear'] == endyear]
    data_by_month_end = data_by_year_end.loc[data_by_year_end['startmonth'] == endmonth]
    endindex = data_by_month_end.index[-1]
    df = data.ix[startindex:endindex, :]
    df = df.reset_index(range(df.shape[0]))
    return df


def check(yr, month):
    """
    The function is going to check the input from user.
    It only allows user to input date from 2013/7 to 2015/10.
    """

    if yr == '2013':
        if month in [str(i) for i in range(7,13)]:
            return True
    elif yr == '2014':
        if month in [str(i) for i in range(1,13)]:
            return True
    elif yr == '2015':
        if month in [str(i) for i in range(1,11)]:
            return True
    else:
        return False

def RepresentsInt(s):
    """
    The function takes a tring input and returns a boolean value: if the string can be converted to an integer, Return True.
    """

    try:
        int(s)
        return True
        
    except ValueError:
        return False

