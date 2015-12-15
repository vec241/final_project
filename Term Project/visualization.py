import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def extract(test_fill):
    '''
    This function parses the date column of the input data into a datetime type variable with which we can generate a number vs.date plot.
    '''
    dates = test_fill['Date']
    sales = test_fill['Sales']
    return dates, sales

def generate_plot(test_fill):
    '''
    This function generates a plot from the input dataframe, with dates on the x-axis, and predicted sales on the y-axis.
    '''
    dates, sales = extract(test_fill)
    fig = plt.figure()
    plt.plot_date(x=dates, y=sales, ls='-')
    fig.autofmt_xdate(rotation=45)
    ax = fig.add_subplot(111)
    plt.grid(True)
    plt.ylabel('Waterlevel (m)')
    plt.title('Sales Prediction of Store ' + format(test_fill['Store'].unique()[0]))
    plt.savefig('prediction_sales_of_Store_{}.png'.format(test_fill['Store'].unique()[0]))
