"""The dataloader module creates a snow.txt file from a larger set of text files
then loads the snow.txt file into a dataframe. Once the data is loaded into the
dataframe, functions clean the and prepare the dataframe for analysis."""

#author: Matthew Dunn
#netID: mtd368
#date: 12/12/2015

from dataloader import loaddata, monthlytextweatherdatamunger, staiondatamunger

def powederhoundinitializer():
    loaddata()
    weathervaluesnorthamerica = monthlytextweatherdatamunger()
    stations = staiondatamunger()
    print 'Powderhound Program is intialized. Please enter "quit" at any point to exit.\n'
    return weathervaluesnorthamerica, stations
