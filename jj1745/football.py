'''
Created on 11/11/2015

@author: jj1745

Contains the main program
'''
import sys
from interactions import askTeam, displayTeams, displaySeasons, askSeason


if __name__ == '__main__':
    
    title = 'Barclays Premier League Analysis Program: 2009 - 2014'
    intro = 'Hi! This program allows you to get team reports and check league table for clubs in BPL.'
    menu = 'Enter: \n 0 to exit the program \n 1 to check team reports \n 2 to check league table \n'
    
    print title
    print intro
    print ''
    
    while True:
        try:
            option = raw_input(menu)
            if option == '1':
                print 'loading... \n'
                displayTeams()
                askTeam()
            
            elif option == '2':
                print 'loading... \n'
                displaySeasons()
                askSeason()
                
            elif option == '0':
                # exit the program
                break
            
            else:
                print 'Sorry, your input is not valid! \n'
        
        except (EOFError, KeyboardInterrupt):
            print 'Program Terminated'
            sys.exit()
    
    print 'Thanks for using this program. Bye!'
    
    


