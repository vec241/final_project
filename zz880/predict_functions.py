import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from modeling_functions import *
import math
import sys

# function used to predict the probability of an item will be sold
def predict_logistic(covariate_list,logistic_fit):
    logistic_coef = logistic_fit.coef_[0]
    logistic_intercept = logistic_fit.intercept_
    temp = np.dot(covariate_list,logistic_coef) + logistic_intercept
    probability = 1 - 1/(1+math.exp(temp))
    print "The probability of the item to be successfully sold is", probability


# function used to predict the final sale price of an item
def predict_linear(covariate_list,linear_fit):
    linear_coef = linear_fit.coef_
    linear_intercept = linear_fit.intercept_
    LogFinalPricePercent = np.dot(covariate_list,linear_coef) + linear_intercept
    FinalPrice = math.exp(LogFinalPricePercent) * math.exp(covariate_list[2])
    print "The expected final sale price is", FinalPrice

# function used to enter prediction data and organize the input covariates for prediction
def prediction_input():
    print "Enter the information of the item you want to sell by the following instructions\nEnter quit to exit at any time\n"
    AvgPrice = raw_input("Enter the average price of the item you want to sell in market\n")
    if AvgPrice == "quit":
        sys.exit()
    else:
        AvgPrice = float(AvgPrice)

    AuctionMedianPrice = raw_input("Enter the median price of the item you want to sell in market\n")
    if AuctionMedianPrice == "quit":
        sys.exit()
    else:
        AuctionMedianPrice = float(AuctionMedianPrice)

    StartingBid = raw_input("Enter the initial bid price\n")
    if StartingBid == "quit":
        sys.exit()
    else:
        StartingBid = float(StartingBid)

    AuctionCount = raw_input("Enter the number of same items you want to sell listed in market\n")
    if AuctionCount == "quit":
        sys.exit()
    else:
        AuctionCount = float(AuctionCount)

    AuctionSaleCount = raw_input("Enter the number of same items you want to sell listed in market resulting in sale\n")
    if AuctionSaleCount == "quit":
        sys.exit()
    else:
        AuctionSaleCount = float(AuctionSaleCount)

    SellerAuctionCount = raw_input("Enter the number items you have ever listed\n")
    if SellerAuctionCount == "quit":
        sys.exit()
    else:
        SellerAuctionCount = float(SellerAuctionCount)

    SellerClose = raw_input("Enter the number of items you have ever listed resulting in sale\n")
    if SellerClose == "quit":
        sys.exit()
    else:
        SellerClose = float(SellerClose)

    covariate_list = []
    covariate_list.append(math.log(StartingBid/AvgPrice))
    covariate_list.append(math.log(SellerClose/SellerAuctionCount))
    covariate_list.append(math.log(AvgPrice))
    covariate_list.append(math.log(AuctionCount))
    covariate_list.append(math.log(AuctionSaleCount))
    covariate_list.append(math.log(SellerAuctionCount))
    covariate_list.append(math.log(AuctionMedianPrice))
    return(covariate_list)
