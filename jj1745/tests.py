'''
Created on 12/10/2015

@author: jj1745

test functions in the Team class because they are the core functions to perform data analysis
'''
import unittest
from teams import Team


class Test(unittest.TestCase):


    def test_TeamFunctions(self):
        # create a sample team to help us check functions 
        t1 = Team('t1','s1',['A','B','C'],[2,3,1],[1,3,2],[1,0,1])

        # this team win in the 1st round, draw in the second, and lose in the third
        self.assertEqual(3, t1.getPoints(1)) # 3 points after 1st round
        self.assertEqual(4, t1.getPoints(2))
        self.assertEqual(4, t1.getPoints(3))
        
        # test goal scored functions
        self.assertEqual(2, t1.getGoalScored(1))
        self.assertEqual(5, t1.getGoalScored(2))
        self.assertEqual(6, t1.getGoalScored(3))
        
        self.assertEqual(1, t1.getGoalConceded(1))
        self.assertEqual(4, t1.getGoalConceded(2))
        self.assertEqual(6, t1.getGoalConceded(3))
        
        self.assertEqual(1, t1.getGoalDifference(1))
        self.assertEqual(1, t1.getGoalDifference(2))
        self.assertEqual(0, t1.getGoalDifference(3))
        
        
        # test record functions
        self.assertEqual([1,0,0], t1.getRecord(1))
        self.assertEqual([1,1,0], t1.getRecord(2))
        self.assertEqual([1,1,1], t1.getRecord(3))
       
        
        # test largest difference
        self.assertEqual([0,2], t1.getLargestDifference())
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()