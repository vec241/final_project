'''
Created on Dec 2, 2015

@author: rjw366
'''
import unittest
import interactionWithUser as ui
import recruitingData as rd


class Test(unittest.TestCase):

    def test_checkForExit(self):
        self.assertTrue(ui.checkForExit("exit"))
        self.assertTrue(ui.checkForExit("quit"))
        self.assertTrue(ui.checkForExit("EXIT"))
        self.assertTrue(ui.checkForExit("  exit    "))
        self.assertFalse(ui.checkForExit("anything"))
        self.assertFalse(ui.checkForExit("  ELSE  1"))
        pass
    
    def test_getAndValidateType(self):
        #Tried importing mock to test the user input and exception raising
        #Instead it required user input
        #Would do same test structuce for year input check
#         self.assertEquals(ui.CUMU_CONSTANT, ui.getAndValidateType())  #cumu
#         self.assertEquals(ui.YEAR_CONSTANT, ui.getAndValidateType())  #year
#         self.assertEquals(ui.YEAR_CONSTANT, ui.getAndValidateType()) #YEAR-
#         self.assertEquals(ui.CUMU_CONSTANT, ui.getAndValidateType()) #   CUMULATIVE    
#         self.assertRaises(ValueError, ui.getAndValidateType()) #yum
        pass
    
    def test_cumu_latsLongs(self):
        loadedData = rd.recruitingData("candidate_info_v2.csv")
        lats,longs = loadedData.getLatsAndLongsForYear(2007)
        self.assertGreater(len(lats), 0)
        self.assertGreater(len(longs), 0)
        pass
    
    def test_yearly_latsLongs(self):
        loadedData = rd.recruitingData("candidate_info_v2.csv")
        lats,longs = loadedData.getLatsAndLongsForYearCumulative(2007)
        self.assertGreater(len(lats), 0)
        self.assertGreater(len(longs), 0)
        pass


if __name__ == "__main__":
    unittest.main()