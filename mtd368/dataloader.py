"""The dataloader module creates a snow.txt file from a larger set of text files
then loads the snow.txt file into a dataframe. Once the data is loaded into the
dataframe, functions clean the and prepare the dataframe for analysis."""

#author: Matthew Dunn
#netID: mtd368
#date: 12/12/2015

import os
import numpy as np
import pandas as pd

def loaddata():
    newfile = os.path.isfile("snow.txt")
    if newfile == False:
        print "Creating snow.txt file from 2.5GB of NOAA text data, this could take a min........\n"
        weathermeasurementtypefilebuilder() # this can be run each time or just once beacause it creates a text file with all the data for a specific precipitation type, currently set to SNOW.

def weathermeasurementtypefilebuilder ():
    dataDirectoryPath = os.path.join(os.path.dirname(__file__), os.pardir, 'ghcnd_hcn')
    newfile = open("snow.txt", 'w')
    for i in os.listdir(dataDirectoryPath):
        filename = dataDirectoryPath+'/'+i
        infile = open(filename)
        for line in infile:
            element = line[17:21]
            if element == 'SNOW':
                newfile.write(line)
        infile.close()
    newfile.close()

def monthlytextweatherdatamunger ():
    print "Loading 344MB of text data from snow.txt file data into dataframe, this could take a min...............\n"
    precipitationFileName = 'snow.txt'
    splits = [[0,11],[11,15],[15,17],[17,21],[21,26],[29,34],[37,42],[45,50],[53,58],[61,66],[69,74],[77,82],[85,90],[93,98],[101,106],[109,114],[117,122],[125,130],[133,138],[141,146],[149,154],[157,162],[165,170],[173,178],[181,186],[189,194],[197,202],[205,210],[213,218],[221,226],[229,234],[237,242],[245,250],[253,258],[261,266]]
    monthlyWeather = splitter(splits, precipitationFileName)
    monthlyWeather.columns = ['Station','Year','Month','Snow','Day01','Day02','Day03','Day04','Day05','Day06','Day07','Day08','Day09','Day10','Day11','Day12','Day13','Day14','Day15','Day16','Day17','Day18','Day19','Day20','Day21','Day22','Day23','Day24','Day25','Day26','Day27','Day28','Day29','Day30','Day31']
    monthlyWeather[['Month','Day01','Day02','Day03','Day04','Day05','Day06','Day07','Day08','Day09','Day10','Day11','Day12','Day13','Day14','Day15','Day16','Day17','Day18','Day19','Day20','Day21','Day22','Day23','Day24','Day25','Day26','Day27','Day28','Day29','Day30','Day31']] = monthlyWeather[['Month','Day01','Day02','Day03','Day04','Day05','Day06','Day07','Day08','Day09','Day10','Day11','Day12','Day13','Day14','Day15','Day16','Day17','Day18','Day19','Day20','Day21','Day22','Day23','Day24','Day25','Day26','Day27','Day28','Day29','Day30','Day31']].astype(float)
    monthlyWeather.replace(to_replace=-9999, value=np.nan, inplace=True)
    monthlyWeather['UniqueStationByYear'] = monthlyWeather['Station']+monthlyWeather['Year']
    monthlyWeather.set_index(monthlyWeather.UniqueStationByYear, inplace=True)
    monthlyWeather = monthlyWeather.drop('UniqueStationByYear',axis=1)
    return monthlyWeather

def staiondatamunger():
    print "Loading Sation data into dataframe...............\n"
    stationsFileName = 'ghcnd-stations.txt'
    splits = [[0,11],[12,20],[21,30],[31,37],[38,40],[41,71],[72,75],[76,79],[80,85]]
    weatherStations = splitter(splits, stationsFileName)
    weatherStations.columns = ['Station', 'LAT', 'LONG', 'ELEV', 'STATE', 'NAME', 'GSNFLAG','HCNFLAG','WMOID']
    weatherStations = weatherStations.set_index('Station')
    return weatherStations

def splitter(splits, fileToBeSplitName):
    fileToBeSplitData = pd.read_csv(fileToBeSplitName, delimiter='\n', dtype=str, squeeze=True, header=None)
    splitDataRepository = pd.DataFrame([])
    for i,j in splits:
        splitname = "split["+str(i)+':'+str(j)+']'
        splitDataRepository[splitname] = fileToBeSplitData.str[slice(i,j)]
    return splitDataRepository
