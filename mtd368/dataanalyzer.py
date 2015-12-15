"""The dataanalyzer module handles the majority of data analysis and summarization of
statistics for user analysis."""

#author: Matthew Dunn
#netID: mtd368
#date: 12/12/2015

import os
import numpy as np
import pandas as pd
import datetime
from datemanager import numberOfDaysinStartMonth

class snowAnalyzer (object):
    def __init__ (self, weather, weekstartdate, weekenddate, deviationpenalty, unittype):
        self.weekstartdate = weekstartdate
        self.weekenddate = weekenddate
        self.weather = weather
        self.deviationpenalty = deviationpenalty
        self.unittype = unittype

    def skiScoreSummarizer(self):
        groupedByMeanPeriods = self.weeklySummaryMetrics()
        groupedByMeanPeriodsProcessed = []
        for i in groupedByMeanPeriods:
            groupedByMeanUnitAdjusted = self.unitConverter(i)
            groupedByMeanUnitAdjusted['AverageScore'] = (groupedByMeanUnitAdjusted['mean']/(groupedByMeanUnitAdjusted['std']*self.deviationpenalty)) # compute the calculation for our score of each location
            groupedByMeanUnitAdjustedSorted = groupedByMeanUnitAdjusted.sort_values('AverageScore', ascending=False, inplace=False) # sort by the AverageScore
            groupedByMeanPeriodsProcessed.append(groupedByMeanUnitAdjustedSorted.head())
        return groupedByMeanPeriodsProcessed

    def unitConverter(self, groupedByMean):
        if self.unittype == 'inch':
            return groupedByMean*0.0393701
        return groupedByMean

    def weeklySummaryMetrics(self):
        summaryWeekMetricsPeriods = self.weeklyMetrics()
        weeklyMetricsThreePeriods = []
        for i in summaryWeekMetricsPeriods:
            summaryWeekMetricsTransposed = i.T
            groupbysummean = summaryWeekMetricsTransposed.groupby(level=0).mean()
            groupbysummeanTransposed = groupbysummean.T
            weeklyMetricsThreePeriods.append(groupbysummeanTransposed)
        return weeklyMetricsThreePeriods

    def weeklyMetrics(self):
        weeklyMetrics = self.builddataframeforgivenweeks()
        weeklyMetrics['StationsTemp'] = weeklyMetrics.index
        weeklyMetricsPrepped = self.stationAndYearSlicer(weeklyMetrics)
        weeklyMetricsPeriods = []
        for i in weeklyMetricsPrepped:
            weeklyMetricsSummarizedTemp = i.pivot_table(index=['Station'],aggfunc=[np.mean,np.std,np.max])
            weeklyMetricsPeriods.append(weeklyMetricsSummarizedTemp)
        return weeklyMetricsPeriods

    def stationAndYearSlicer(self, weeklyMetricsToBeSliced):
        stationSplit = weeklyMetricsToBeSliced['StationsTemp']
        onlyStations = stationSplit.str[:-4]
        years = stationSplit.str[11:]
        weeklyMetricsToBeSliced['Station'] = onlyStations
        weeklyMetricsToBeSliced['Year'] = years
        weeklyMetricsToBeSliced['Year'] = weeklyMetricsToBeSliced['Year'].astype(int)
        yearRangePeriodsPrepped = self.yearlist()
        weeklyMetricsPeriodsPrepped = []
        for i in range(3):
            slicedWeeklyMetricsTemp = weeklyMetricsToBeSliced.ix[weeklyMetricsToBeSliced.Year >= yearRangePeriodsPrepped[i]]
            slicedWeeklyMetricsTemp = slicedWeeklyMetricsTemp.drop(['StationsTemp','Year'],axis=1,inplace=False)
            weeklyMetricsPeriodsPrepped.append(slicedWeeklyMetricsTemp)
        return weeklyMetricsPeriodsPrepped

    def yearlist(self):
        yearRangePeriods = [25, 50, 0] # leave third item zero for the calculation across all years.
        for i in range(2):
            yearPeriodTemp = datetime.datetime.now().year - yearRangePeriods[i]
            yearRangePeriods[i] = yearPeriodTemp
        return yearRangePeriods

    def builddataframeforgivenweeks (self):
        if self.datesofweekinsamemonthchecker(self.weekstartdate, self.weekenddate) == 1:
            return self.skiPeriodSplitter(self.weekstartdate.month, self.weekstartdate.day, self.weekenddate.day)
        else:
            numberofdaysinstartmonth, startMonthLastDay = numberOfDaysinStartMonth(self.weekstartdate) # send dates to weeksacrossmonthsmanager to get the exact day intervals for each month
            dateOfStartDay = startMonthLastDay - numberofdaysinstartmonth
            return self.skiPeriodMerger(startMonthLastDay)

    def skiPeriodMerger (self, startEndDate): # merges two dataframes together for case were ski week extends across two months.
        startSkiPeriod = self.skiPeriodSplitter(self.weekstartdate.month, self.weekstartdate.day, startEndDate)
        endSkiPeriod = self.skiPeriodSplitter(self.weekenddate.month, 01, self.weekenddate.day)
        return pd.concat([startSkiPeriod, endSkiPeriod], axis=1)

    def skiPeriodSplitter (self, month, startdate, enddate):
        weekofrawdata = self.weather.ix[self.weather.Month == int(month)]                        # select only the rows for which the month matches.
        startdatecolumnname = 'Day'+str(startdate).zfill(2)                                     # build string to use in fancy indexing
        enddatecolumnname = 'Day'+str(enddate).zfill(2)                                         # build string to use in fancy indexing
        return weekofrawdata.loc[:,startdatecolumnname:enddatecolumnname]                       # slice datframe to get the columns for the days of interest.

    def datesofweekinsamemonthchecker(self, weekstartdate, weekenddate):                        # checks if the start date and end date are in the same month.
        if weekstartdate.month == weekenddate.month:
            return 1
        return 0
