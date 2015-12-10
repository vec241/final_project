'''
Created on 11/27/2015

@author: jj1745

The module where we read and process user inputs. 
'''
import sys
from league import *
from loader import processData


def getAllTeams():
    '''
    get all teams that have played in the last 5 seasons in the premier league
    @return: the set of teams 
    '''
    all_names = set()
    all_seasons = ['09-10','10-11','11-12','12-13','13-14']
    for season in all_seasons:
        info_list = processData(season)
        names = getTeamNames(info_list)
        all_names = all_names.union(names)
        
    return all_names
   

def displayTeams():
    '''
    display all teams to help users
    '''
    all_names = getAllTeams()
    size = len(all_names)
    print 'We have the following ' + str(size) + ' teams appearing in the BPL during 2009 - 2014: \n'
    text = ''
    for n in all_names:
        text = text + n + '\n'
    
    print text 
  
    
def askTeam():
    '''
    ask for a particular team from the user
    '''
    all_names = getAllTeams()
    try:    
        user_input = raw_input('Which team are you interested in checking? Enter a name from the list above. Team reports and analysis will be provided.')
        if user_input in all_names:
            print 'generating report and plots... \n'
            # perform team analysis, create folder, and save files
            makeDirectory(user_input)
            generateReport(user_input)
            plotHomeAwayRecords(user_input)
            plotHomeAwayStat(user_input)
        
            print 'Awesome! Team report and plots have been saved. Please check the folder with name ' + user_input + '. \n'
             
        else:
            print 'Sorry! The input is not valid. Please enter a valid team name. Note that the input is case-sensitive.\n'
            askTeam()
            
    except (EOFError, KeyboardInterrupt):
        print 'Program Terminated'
        sys.exit()


def displaySeasons():
    '''
    display all seasons to help users
    '''
    all_seasons = ['09-10','10-11','11-12','12-13','13-14']
    print 'You can check the league table at any round for the following 5 seasons: \n'
    text = ''
    for s in all_seasons:
        text = text + s + '\n'
    
    print text


def askRound(season):
    '''
    ask round from the user
    @param season: the input season from the user
    '''
    all_rounds = []
    for i in range(1,39):
        all_rounds.append(str(i))
    
    try:
        round_input = raw_input('Which round would you like to check? Please enter an integer from 1 to 38.')
        if round_input in all_rounds:
            print 'generating table... \n'
            round = int(round_input)
            info_list = processData(season)
            table = getTable(season, round, info_list)
            print table
            print ''
        else:
            print 'Sorry! The input is not valid. Please enter a valid round'
            askRound(season)
    
    except (EOFError, KeyboardInterrupt):
        print 'Program Terminated'
        sys.exit()

        
def askSeason():
    '''
    ask season from the user
    '''
    all_seasons = ['09-10','10-11','11-12','12-13','13-14']
            
    try:
        user_input = raw_input('Which season would you like to look at? Enter a season from the list above.')
        if user_input in all_seasons:
            askRound(user_input)
        else:
            print 'Sorry! The input is not valid. Please enter a valid season.\n'
            askSeason()
            
    except (EOFError, KeyboardInterrupt):
        print 'Program Terminated'
        sys.exit()
               
    
    