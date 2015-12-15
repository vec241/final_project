import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from modeling_functions import *
from preprocess import *
from evaluation_functions import *
from predict_functions import *
import unittest


class TestFinalProject(unittest.TestCase):

    # Test if function split_data used first 2500 samples as train and the remaining as test
    def test_split_data(self):
        data = pd.read_csv("EbayAuctionData.csv")
        total = len(data.axes[0])
        train, test = split_data(data)
        self.assertEqual(len(train.axes[0]),2500)
        self.assertEqual(len(test.axes[0]),total-2500)

    # Test if function log_transformation works
    def test_log_transformation(self):
        data = pd.read_csv("EbayAuctionData.csv")
        log_data = log_transformation(data)
        true = np.log(data[data.columns[1]])
        self.assertEqual(true[0], log_data.ix[0]["Log PricePercent"])
        self.assertEqual(true[1], log_data.ix[1]["Log PricePercent"])

if __name__ == "__main__":
    unittest.main()