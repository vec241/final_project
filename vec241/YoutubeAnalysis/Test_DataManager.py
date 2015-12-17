from unittest import TestCase
from DataManager import DataManager
import os
import glob
import numpy as np

class Test(TestCase):

    def test_Initialization(self):
        dm=DataManager()
        data = dm.load_data()
        #self.assertFalse(data, np.nan )
        #print np.arange(1,10)
