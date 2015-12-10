'''
Created on 11/14/2015

@author: jj1745

The module with functions that perform analysis on a league level. 
'''
from loader import processData, getTeamInfo
import os
import pandas as p
import numpy as np
import matplotlib.pyplot as plt


def getTeamNames(info_list):
    '''
    get the set of all team names 
    @param info_list: output from the processData function
    @return: the set of all 20 teams in a given season
    '''
    team_list = info_list[0]
    names = set(team_list)
    return names


def createList(season, round, info_list):
    '''
    get detailed information (points, goal difference...) of all 20 teams in the league after certain round
    @param season: a string indicating the input season
    @param round: A positive integer from 1-38; indicate how many rounds have been played
    @param info_list: output from the processData function
    @return: a list of tuples with detailed information 
    '''
    names = getTeamNames(info_list)
    league_list = []
    
    for n in names:
        new_team = getTeamInfo(n, info_list, season)
        pts = new_team.getPoints(round) # points accumulated
        W = new_team.getRecord(round)[0] # number of games won
        D = new_team.getRecord(round)[1] # number of games drawn
        L = new_team.getRecord(round)[2] # number of games lost
        GF = new_team.getGoalScored(round) # goal scored
        GA = new_team.getGoalConceded(round) # goal conceded
        GD = new_team.getGoalDifference(round) # goal difference
        league_list.append((n, pts, W, D, L, GF, GA, GD))
    
    return league_list
    

def getTable(season, round, info_list):
    '''
    produce the league table of 20 teams after certain rounds
    @param season: a string indicating the input season
    @param round: A positive integer from 1-38; indicate how many rounds have been played
    @param info_list: output from the processData function
    @return: a pandas DataFrame of league table
    '''
    league_list = createList(season, round, info_list)
 
    dtype = [('Team','S10'), ('Pts',int), ('W',int), ('D',int), ('L',int), ('GF',int), ('GA',int), ('GD',int)]
    league_array = np.array(league_list, dtype = dtype)
    ranked_list = np.sort(league_array, order=['Pts', 'GD', 'GF'])
    table = p.DataFrame(ranked_list)
    table = table.iloc[::-1] # need to reverse the table 
    table.index = range(1,21)
    
    return table


'''The following functions help to create Team report'''

def makeDirectory(name):
    '''
    Check if a directory for the team has already existed.
    If not, create the directory
    @param name: the input team name
    '''
    directory = './' + name
    if not os.path.exists(directory):
        os.makedirs(directory)

    
def generateReport(name):
    '''
    generate the team report and saves it in the corresponding folder
    @param name: the input team name
    '''
    path = './' + name + '/report.txt'
    
    try:
        report = open(path, 'w')
        report.write('Team Name: ' + name + '\n')
        report.write('\n')
    
        all_seasons = ['09-10','10-11','11-12','12-13','13-14']
        for season in all_seasons:
            info_list = processData(season)
            names = getTeamNames(info_list)
            if name in names:
                # if the team plays in the premier league during the season
                report.write(season + ' Season: \n')
                table = getTable(season, 38, info_list)
                record = table[table.Team == name]
                rank = record.index[0]
                W = record.iloc[0,2]
                D = record.iloc[0,3]
                L = record.iloc[0,4]
                GF = record.iloc[0,5]
                GA = record.iloc[0,6]
                # writes the basic information of the season.
                report.write(name + ' ranks ' + str(rank) + ' this season. ')
                report.write('They win ' + str(W) + ', draw ' + str(D) + ', and lose ' + str(L) + ' games.')
                report.write('\n')
                report.write('They score ' + str(GF) + ' goals and concede ' + str(GA) + ' goals in total.')
                report.write('\n')
            
                team = getTeamInfo(name, info_list, season)
                # write the largest victory of the season
                idx_diff = team.getLargestDifference()
                report.write('The largest victory is against ' + team.opponents[idx_diff[0]] + '. ')
                report.write('The score is ' + str(team.goals_scored[idx_diff[0]]) + '-')
                report.write(str(team.goals_conceded[idx_diff[0]]) + '. \n')
                # write the largest defeat of the season
                report.write('The largest defeat is against ' + team.opponents[idx_diff[1]] + '. ')
                report.write('The score is ' + str(team.goals_scored[idx_diff[1]]) + '-')
                report.write(str(team.goals_conceded[idx_diff[1]]) + '. \n')
                 
                report.write('\n')
        
        report.close()
    
    except IOError:
        print 'Error occurs when writing the report file'
    

def plotHomeAwayStat(name):
    '''
    generate relevant plots and saves them in the corresponding folder
    @param name: the input team name
    '''
    plt.clf() # clear previous figures
    path = './' + name + '/home_away_stats'
    
    all_seasons = ['09-10','10-11','11-12','12-13','13-14']
    
    # a helper counter
    count = 0
    idx = [] 
    for season in all_seasons:
        info_list = processData(season)
        names = getTeamNames(info_list)
        if name in names:
            count = count + 1
            idx.append(season)
    
    # initializes a matrix of the corresponding size
    stats = np.zeros((count, 4))
    
    count = 0
    for season in all_seasons:
        info_list = processData(season)
        names = getTeamNames(info_list)
        if name in names:
            team = getTeamInfo(name, info_list, season)
            stats[count,] = team.computeAvgGoal()
            count = count + 1
    
    colnames = ['Score-Home', 'Concede-Home', 'Score-Away', 'Concede-Away']
    df = p.DataFrame(stats, index = idx, columns = p.Index(colnames,name = 'Avg. Goals per Game'))
    df.plot(kind = 'bar')
    plt.legend(prop={'size':12})
    plt.title('Average Goals Scored and Conceded per Game of ' + name)
    plt.xlabel('Season')
    plt.ylabel('Average Goals per Game')
    plt.savefig(path)


def plotHomeAwayRecords(name):
    '''
    generate relevant plots and saves them in the corresponding folder
    @param name: the input team name
    '''
    plt.clf()
    path = './' + name + '/home_away_records'
    
    all_seasons = ['09-10','10-11','11-12','12-13','13-14']
    # a helper counter
    count = 0
    idx = [] 
    for season in all_seasons:
        info_list = processData(season)
        names = getTeamNames(info_list)
        if name in names:
            count = count + 1
            idx.append(season)
    
    # initialize array for home and away record
    record = np.zeros((count,2))
    
    count = 0
    for season in all_seasons:
        info_list = processData(season)
        names = getTeamNames(info_list)
        if name in names:
            team = getTeamInfo(name, info_list, season)
            r_1 = team.getHomeAwayRecord()[0,:] # home record
            r_2 = team.getHomeAwayRecord()[1,:] # away record
            record[count,0] = np.average(r_1, weights = [3,1,0])
            record[count,1] = np.average(r_2, weights = [3,1,0])
            
            count = count + 1
    
    colnames = ['Home', 'Away']
    df = p.DataFrame(record, index=idx, columns=colnames)
        
    df.plot(kind = 'barh', stacked = True)
    plt.title('Home and Away Records of ' + name)
    plt.xlabel('Average Points Obtained per Game')
    plt.ylabel('Season')
    plt.savefig(path)
    
    
    
    
    
            
    
    
        
    