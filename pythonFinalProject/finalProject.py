'''
Created on Dec 15, 2015

@author: rjw366

Using a recruiting dataset one can enter in a type of search and a year to see a plot 
over the US of where candidates have been recruited from
'''
import recruitingData as rd
import interactionWithUser as ui
import sys

if __name__ == '__main__':
    #Load in dataset
    loadedData = rd.recruitingData("candidate_info_v2.csv")
    #Explain to user
    ui.explainProgram()
    while(input != "quit" and input != "exit"):
        try:
            #Get type and year of search
            typeOfSearch = ui.getAndValidateType()
            yearOfSearch = ui.getAndValidateYear()
            #Perform actual search and print out plot
            lats, longs = loadedData.startSearch(typeOfSearch, yearOfSearch)
            loadedData.printPlotBasemap(longs, lats)
        except ValueError:
            #Catches input errors, explains again, restarts input loop
            print("There was a problem with your input. I'll explain again")
            ui.explainProgram()
        except KeyboardInterrupt:
            #Catches keyboard interrupt and safely quits
            print("I noticed you tried killing me with the keyboard.")
            print("Well I'll beat you to it!")
            sys.exit()       