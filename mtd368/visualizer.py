"""The visualizer module handles the process of generating the charts needed to evaluate
where a person should ski.  It does a small amount of data prep specific to the visualization
process, but is primarily concerned focused on visualizing the data."""

#author: Matthew Dunn
#netID: mtd368
#date: 12/12/2015

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class visualizationofskidata(object):
    def __init__(self, mergedSkiDataPeriods, startDate, endDate):
        self.mergedSkiDataPeriods = mergedSkiDataPeriods
        self.startDate = startDate
        self.endDate = endDate

    def dataprep (self):
        locationNames, bigdumpmean, bigdumpstd, ind = [], [], [], []
        for i in self.mergedSkiDataPeriods:
            skiDataPrepped = i.dropna(axis=0, how='any')
            skiDataPrepped.set_index('StateCity', inplace=True)
            bigdumpstd.append(skiDataPrepped['std'].values)
            bigdumpmean.append(skiDataPrepped['mean'].values)
            locationNames.append(skiDataPrepped.index)
            ind.append(np.arange(len(skiDataPrepped['std'])))  # the x locations for the groups for plotting.
        return locationNames, bigdumpmean, bigdumpstd, ind

def skiAreaBarChart(skiperiodscores, skiperiodstdDeviations, numberOfItems, locationNames):
    xmaxvalue = xmaxgenerator(skiperiodscores)
    width = 0.35
    plt.figure(1, tight_layout=False, figsize=(12,12))
    plt.subplots_adjust(bottom=0.1, left=0.3, top=0.9, hspace=0.5, wspace=None)
    plt.suptitle('ALL HISTORICAL NOAA DATA', fontsize=20)
    titles = ['Two Weeks BEFORE to Entered Date','One Week BEFORE to Entered Date', 'Week of Entered Date', 'One Week AFTER to Entered Date', 'Two Weeks AFTER to Entered Date']
    for i in range(5):
        plt.subplot(5, 1, i+1)
        plt.title(titles[i])
        plt.barh(numberOfItems[i][2], skiperiodscores[i][2], width, align='center', color='r', xerr=skiperiodstdDeviations[i][2], alpha=0.4)
        plt.yticks(numberOfItems[i][2],locationNames[i][2])
        plt.xlim(0,xmaxvalue)
        plt.grid(True)
    plt.show()

def last50YearsData(skiperiodscores, skiperiodstdDeviations, numberOfItems, locationNames):
    xmaxvalue = xmaxgenerator(skiperiodscores)
    width = 0.35
    plt.figure(2, tight_layout=False, figsize=(12,12))
    plt.subplots_adjust(bottom=0.1, left=0.3, top=0.9, hspace=0.5, wspace=None)
    plt.suptitle('LAST 50 YEARS NOAA DATA', fontsize=20)
    titles = ['Two Weeks BEFORE to Entered Date','One Week BEFORE to Entered Date', 'Week of Entered Date', 'One Week AFTER to Entered Date', 'Two Weeks AFTER to Entered Date']
    for i in range(5):
        plt.subplot(5, 1, i+1)
        plt.title(titles[i])
        plt.barh(numberOfItems[i][1], skiperiodscores[i][1], width, align='center', color='r', xerr=skiperiodstdDeviations[i][1], alpha=0.4)
        plt.yticks(numberOfItems[i][1],locationNames[i][1])
        plt.xlim(0,xmaxvalue)
        plt.grid(True)
    plt.show()

def last25YearsData(skiperiodscores, skiperiodstdDeviations, numberOfItems, locationNames):
    xmaxvalue = xmaxgenerator(skiperiodscores)
    width = 0.35
    plt.figure(3, tight_layout=False, figsize=(12,12))
    plt.subplots_adjust(bottom=0.1, left=0.3, top=0.9, hspace=0.5, wspace=None)
    plt.suptitle('LAST 25 YEARS NOAA DATA', fontsize=20)
    titles = ['Two Weeks BEFORE to Entered Date','One Week BEFORE to Entered Date', 'Week of Entered Date', 'One Week AFTER to Entered Date', 'Two Weeks AFTER to Entered Date']
    for i in range(5):
        plt.subplot(5, 1, i+1)
        plt.title(titles[i])
        plt.barh(numberOfItems[i][1], skiperiodscores[i][1], width, align='center', color='r', xerr=skiperiodstdDeviations[i][1], alpha=0.4)
        plt.yticks(numberOfItems[i][1],locationNames[i][1])
        plt.xlim(0,xmaxvalue)
        plt.grid(True)
    plt.show()

def xmaxgenerator(skiperiodscores):
    maxskiScores = []
    for i in range(5):
        maxskiScores.append(skiperiodscores[i][2])
    xmax = sorted(map(max, zip(*maxskiScores)))
    xmax = np.ceil(xmax[-1])+5  # Ensure the chart is large enough for the largest value.
    return xmax
