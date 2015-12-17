"""This is a program that allows users to analyze the average snowfall by day across the
lower 48 states. The program uses NOAA data sets and allows the user to evaluate different
periods of the year to ski."""

#author: Matthew Dunn
#netID: mtd368
#date: 12/12/2015

from dataloader import *
from dataanalyzer import *
from locationizer import *
from visualizer import *
from userinputmanager import *
from datemanager import *
from intializer import powederhoundinitializer

def main():
    try:
        weathervaluesnorthamerica, stations = powederhoundinitializer()
        while True:
            unittype, skidate, deviationpenalty = userinput()
            possibleSkiWeeks = datesrangenerator(skidate)
            scoresforperiods, stdDeviationsforperiods, numberOfItemsforperiods, locationNamesforperiods = [], [], [], []
            for startDate,endDate in possibleSkiWeeks:
                oneWeekOfSking = snowAnalyzer(weathervaluesnorthamerica, startDate, endDate, deviationpenalty, unittype).skiScoreSummarizer()
                ratedSkiPeriodWithLocation = skiresortlocater(oneWeekOfSking, stations).mergedatatoanalyze()
                locationNames, scores, stdDeviations, numberOfItems = visualizationofskidata(ratedSkiPeriodWithLocation, startDate, endDate).dataprep()
                scoresforperiods.append(scores)
                stdDeviationsforperiods.append(stdDeviations)
                numberOfItemsforperiods.append(numberOfItems)
                locationNamesforperiods.append(locationNames)
            skiAreaBarChart(scoresforperiods, stdDeviationsforperiods, numberOfItemsforperiods, locationNamesforperiods)
            last50YearsData(scoresforperiods, stdDeviationsforperiods, numberOfItemsforperiods, locationNamesforperiods)
            last25YearsData(scoresforperiods, stdDeviationsforperiods, numberOfItemsforperiods, locationNamesforperiods)
    except KeyboardInterrupt, ValueError:
        print "\n Interrupted!"
    except EOFError:
        print "\n Interrupted!"

if __name__ == '__main__':
    main()
