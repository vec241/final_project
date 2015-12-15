"""The locationizer module merges NOAA analyzed data with location data of the
stations where the data was recorded. This enables the program to present the
state and city where the best skiing is in the united states."""

#author: Matthew Dunn
#netID: mtd368
#date: 12/12/2015

import os
import numpy as np
import pandas as pd

class skiresortlocater(object):

    def __init__ (self, rankedPeriodsData, stations):
        self.rankedPeriodsData = rankedPeriodsData
        self.stations = stations

    def mergedatatoanalyze(self):
        mergedPeriodDataAndStations = []
        for i in self.rankedPeriodsData:
            weatherandstations = pd.merge(i, self.stations, how='left', left_index=True, right_index=True)
            weatherandstations['StateCity'] = weatherandstations['STATE']+" "+weatherandstations['NAME']
            mergedPeriodDataAndStations.append(weatherandstations)
            # print list(weatherandstations.columns.values)
        return mergedPeriodDataAndStations

