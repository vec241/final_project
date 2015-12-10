'''
Created on 11/11/2015

@author: jj1745

The module where we read and process data.  
'''
import openpyxl as px
from teams import Team


def loadData(season):
    '''
    load the data set using openpyxl package
    @param season: a string indicating the input season
    @return: the loaded sheet 
    '''
    try:
        filename = './data/premier_league_' + season + '.xlsx'
        W = px.load_workbook(filename,use_iterators=True)
        sheet = W.get_sheet_by_name(name = 'Sheet1')     
        return sheet
    except IOError:
        print 'The data is not in the proper directory. Please check'


def processData(season):
    '''
    read the sheet line by line; store the data into 4 different lists
    @param season: a string indicating the input season
    @return: a list of 4 categories of information
    '''
    sheet = loadData(season) #load the data of a given season 
    
    home_team_list = []
    away_team_list = []
    home_score = []
    away_score = []
    count = 0
    for row in sheet.iter_rows():
        for item in row:
            if count >= 5:
                # ignore the first row because that's the header
                pos = count%5 # every row has 5 items
                
                if pos == 1:
                    # this is the position of home team
                    home_team = item.internal_value
                    home_team = home_team.encode('ascii')
                    home_team_list.append(home_team)
                elif pos == 2:
                    # this is the position of away team
                    away_team = item.internal_value
                    away_team = away_team.encode('ascii')
                    away_team_list.append(away_team)
                elif pos == 3:
                    # this is the position of the final score
                    text = item.internal_value
                    text = text.encode('ascii')
                    score = text.split('-')
                    home_score.append(int(score[0]))
                    away_score.append(int(score[1]))
            
            count = count + 1
    
    info_list = [home_team_list,home_score,away_team_list,away_score]
    return info_list


def getTeamInfo(team_name, info_list, season):
    '''
    given the name of a team, create a team object with data retrieved from the list
    @param team_name: the name of a football club
    @param info_list: output from the processData function
    @param season: a string indicating the input season
    @return: a Team object  
    '''
    home_team_list = info_list[0]
    home_score = info_list[1]
    away_team_list = info_list[2]
    away_score = info_list[3]
    # get the index of the team at home
    idx_home = [i for i, x in enumerate(home_team_list) if x == team_name]
    # get the index of the team away
    idx_away = [i for i, x in enumerate(away_team_list) if x == team_name]
    idx = sorted(idx_home + idx_away)
    
    opponents = []
    goals_scored = []
    goals_conceded = []
    
    # a list that indicates whether the team is playing at home in each round
    at_home = []
    
    for i in idx:
        if (i in idx_home):
            # meaning this is a home game for the team
            opponents.append(away_team_list[i])
            goals_scored.append(home_score[i])
            goals_conceded.append(away_score[i])
            at_home.append(1)
        else:
            # meaning this is an away game for the team
            opponents.append(home_team_list[i])
            goals_scored.append(away_score[i])
            goals_conceded.append(home_score[i])
            at_home.append(0)
    
    return Team(team_name,season,opponents,goals_scored,goals_conceded, at_home)
    
    

            
    
            
