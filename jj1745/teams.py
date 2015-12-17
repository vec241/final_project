'''
Created on 11/12/2015

@author: jj1745

The module with the Team class.
'''
import numpy as np


class Team(object):
    '''
    Every team in any season in the premier league is an object
    '''

    def __init__(self, team_name, season, opponents, goals_scored, goals_conceded, at_home):
        '''
        Constructor
        '''
        self.team_name = team_name
        self.season = season
        self.opponents = opponents
        self.goals_scored = goals_scored
        self.goals_conceded = goals_conceded
        self.at_home = at_home

    
    def getPoints(self, fixtures):
        '''
        compute points the team obtains 
        @param fixtures: A positive number from 1 to 38; indicate which round the user is considering.
        @return: the total points accumulated by the team 
        '''
        points = 0
        for r in range(fixtures):
            if self.goals_scored[r] > self.goals_conceded[r]:
                # a win gives the team 3 points!
                points = points + 3
            elif self.goals_scored[r] == self.goals_conceded[r]:
                # a draw gives the team 1 point!
                points = points + 1
        
        return points
 
    
    def getGoalScored(self, fixtures):
        '''
        @param fixtures: A positive number from 1 to 38
        @return: the total goals scored by the team after a given round
        '''
        scored = sum(self.goals_scored[:fixtures])
        return scored

    
    def getGoalConceded(self, fixtures):
        '''
        @param fixtures: A positive number from 1 to 38
        @return: the total goals conceded by a team after a given round
        '''
        conceded = sum(self.goals_conceded[:fixtures])
        return conceded
  
    
    def getGoalDifference(self, fixtures):
        '''
        @param fixtures: A positive number from 1 to 38
        @return: the goal difference conceded by a team after a given round
        '''
        goal_difference = self.getGoalScored(fixtures) - self.getGoalConceded(fixtures)
        return goal_difference
 
    
    def getRecord(self, fixtures):
        '''
        @param fixtures: A positive number from 1 to 38
        @return: [wins, draws, losses] record of a team after a given round
        '''
        record = [0,0,0] # [Wins, Draws, Losses]
        for r in range(fixtures):
            if self.goals_scored[r] > self.goals_conceded[r]:
                # win occurs
                record[0] = record[0] + 1
            elif self.goals_scored[r] == self.goals_conceded[r]:
                # draw occurs
                record[1] = record[1] + 1
            else:
                record[2] = record[2] + 1
        
        return record
    
    def getHomeAwayRecord(self):
        '''
        @return: the home and away record [wins, draws, losses] after 38 rounds in a season
        '''
        record = np.array([[0,0,0],[0,0,0]]) # [Wins, Draws, Losses]
        
        for r in range(38):
            if self.goals_scored[r] > self.goals_conceded[r]:
                # win occurs
                if self.at_home[r] == 1:
                    # play at home
                    record[0,0] = record[0,0] + 1
                else:
                    # play away
                    record[1,0] = record[1,0] + 1
            elif self.goals_scored[r] == self.goals_conceded[r]:
                # draw occurs
                if self.at_home[r] == 1:
                    # play at home
                    record[0,1] = record[0,1] + 1
                else:
                    # play away
                    record[1,1] = record[1,1] + 1
            else:
                if self.at_home[r] == 1:
                    # play at home
                    record[0,2] = record[0,2] + 1
                else:
                    # play away
                    record[1,2] = record[1,2] + 1
        
        return record
    
    def computeAvgGoal(self):
        '''
        @return:[avg home goal scored],
                [avg home goal conceded], 
                [avg away goal scored],
                [avg away goal conceded],
                after 38 games in the season
        '''
        goals = np.zeros((4,19))
        idx_h = 0
        idx_a = 0
        for r in range(38):
            if self.at_home[r] == 1:
                goals[0,idx_h] = self.goals_scored[r]
                goals[1,idx_h] = self.goals_conceded[r]
                idx_h = idx_h + 1
            else:
                goals[2,idx_a] = self.goals_scored[r]
                goals[3,idx_a] = self.goals_conceded[r]
                idx_a = idx_a + 1
        
        avg_goals = np.average(goals, axis = 1)
        
        return avg_goals
    
    def getLargestDifference(self):
        '''
        @return: [largest win (round), largest defeat (round)]
        '''
        GF = np.array(self.goals_scored)
        GA = np.array(self.goals_conceded)
        GD = GF - GA
        idx_win = np.argmax(GD)
        idx_loss = np.argmin(GD)
        
        return [idx_win, idx_loss]