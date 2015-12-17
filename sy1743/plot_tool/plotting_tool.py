from __future__ import division
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import operator
from matplotlib.gridspec import GridSpec


# DS-GA 1007 Final Project
# Visualization tool
# Author: Sida Ye

"""
Provide monthly data visualization for citibike by user's requirement

"""

class visualizationTool(object):
    
    def __init__(self, data, year, month):
        self.data = data
        self.year = year
        self.month = month


    def pieplot(self, variable):
        """ 
        Plot pie plot for gender or usertype in certain period
        """

        variable_type = self.data[variable].unique()
        variable_size = []
        if variable == 'gender':
            for i in np.sort(variable_type):
                variable_size.append(round((sum(self.data[variable] == i) / self.data.shape[0] * 100), 2))    # calculate distirbution
            # Gender (Zero=unknown; 1=male; 2=female)
            labels = 'Unknown', 'Male', 'Female'
            sizes = variable_size
            colors = ['lightyellow','lightskyblue', 'lightcoral']
            explode = (0, 0.1, 0.1)  # "explode" the distribution of male and female

            plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                    autopct='%1.1f%%', shadow=True, startangle=90)
            # Set aspect ratio to be equal so that pie is drawn as a circle.
            plt.axis('equal')
            plt.title('Gender Distribution in {}-{}'.format(self.year, self.month), fontsize = 12,y = 1,x=0.12,bbox={'facecolor':'0.8', 'pad':5})
            plt.show()

        elif variable == 'usertype':
            # usertype (Zero=Customer, 1=Subscriber)
            for i in range(2): # change to 0, 1
                variable_size.append(round((sum(self.data[variable] == i) / self.data.shape[0] * 100), 2))    # calculate distribution
            labels = 'Subscriber', 'Customer'
            sizes = variable_size
            colors = ['lightcoral','lightskyblue']
            explode = (0, 0.1)  # only "explode" the subscriber

            plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                    autopct='%1.1f%%', shadow=True, startangle=90)
            # Set aspect ratio to be equal so that pie is drawn as a circle.
            plt.axis('equal')
            plt.title('User Type Distribution in {}-{}'.format(self.year, self.month), fontsize = 12,y = 1,x=0.12,bbox={'facecolor':'0.8', 'pad':5})
            plt.show()
    


    def plot_daily_freq(self, show_mile=False):
        """ 
        Plot bar plot for the daily usage or miles in certain month 
        """
        
        if show_mile == False:
            self.data['startdate'] = [self.data['starttime'][i].split(' ')[0] for i in range(self.data.shape[0])]   # get date end with day
            freq_date = Counter(self.data['startdate']) # calculate number of trips for each day
            sorted_freq_date = sorted(freq_date.items(), key=operator.itemgetter(0)) # sorted by date
            df = pd.DataFrame(sorted_freq_date, columns=['Date', 'freq'])   # convert into dataframe
            df['Date']=sorted(pd.to_datetime(df['Date'], unit='D')) # convert string to datetime format and sorted dataframe by date
            df['Date'] = [str(date).split(' ')[0] for date in df['Date']]   # get date end with day
            df = df.set_index('Date')   # set date as index
            df.plot(kind='bar',legend=False, color='lightblue',alpha=0.8,figsize=(13,9)) # make a bar plot
            plt.ylabel('Usage', fontsize=16) # adjust y label
            plt.xticks(rotation=85) # rotate x ticks
            plt.grid(True)
            plt.title('Daily trips for {}'.format(str(self.year)+'-'+str(self.month).zfill(2))) # add title for the plot
            plt.show()
        elif show_mile == True:
            self.data['startdate'] = [self.data['starttime'][i].split(' ')[0] for i in range(self.data.shape[0])] # get date end with day
            trip_usage = {} # create a dictionary with date as key and miles as value
            for i in self.data['startdate'].unique():
                trip_usage[i] = round(sum(self.data[self.data['startdate'] == i]['tripduration']) * 3.33 / 1000, 2)   # bike speed 3.33m/s          
            df = pd.DataFrame(trip_usage.items(), columns=['Date','mile']) # convert dictionary into dataframe
            df['Date']=sorted(pd.to_datetime(df['Date'], unit='D')) # sorted dataframe by date
            df['Date'] = [str(date).split(' ')[0] for date in df['Date']] # get date end with day
            df = df.set_index(df['Date']) # set index as date
            df = df.drop('Date', 1) # drop original date column
            df.plot(kind='bar',legend=False, color='lightblue',alpha=0.8,figsize=(13,9)) # create bar plot
            plt.ylabel('Miles', fontsize=16)    # adjust y label
            plt.xticks(rotation=85) # rotate xticks
            plt.grid(True)
            plt.title('Miles Traveled Daily for {}'.format(str(self.year)+'-'+str(self.month).zfill(2))) # add title for this plot
            plt.show()
        else:   # handel exception for invalid input format of show_mile
            raise KeyError('Wrong input format for show_mile')






