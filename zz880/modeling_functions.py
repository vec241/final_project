import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression


# Split data into training and testing set
def split_data(data):
    #use first 2500 subjects as training set and the remianing as testing set
    data_train = data.ix[range(2500)]
    data_test = data.ix[2500:]
    return data_train, data_test


# Data preparation for logistic regression
def logistic_prepare(data):
    y = data["QuantitySold"]
    x = data[["Log StartingBidPercent","Log SellerClosePercent","Log AvgPrice","Log AuctionCount","Log AuctionSaleCount"
              ,"Log SellerAuctionCount","Log AuctionMedianPrice"]]
    return x, y

# Data preparation for linear regreaaion
def linear_prepare(data):
    y = data["Log PricePercent"]
    x = data[["Log StartingBidPercent","Log SellerClosePercent","Log AvgPrice","Log AuctionCount","Log AuctionSaleCount"
              ,"Log SellerAuctionCount","Log AuctionMedianPrice"]]
    return x, y

# Fit logistic regression
def logistic_model(x,y):
    logr = LogisticRegression(fit_intercept=True)
    logr.fit(x,y)
    return logr

# Report coefficients of a logistic regression model
def coef_logistic(logistic_fit,data):
    print "Intercept:",logistic_fit.intercept_[0]
    names = list(data.columns)
    coef = logistic_fit.coef_
    for i in range(len(names)):
        print names[i],":",coef[0][i]

# Fit linear regression
def linear_model(x,y):
    lr = LinearRegression(fit_intercept=True)
    lr.fit(x, y)
    return lr

# Report coefficients of a linear regression model
def coef_linear(linear_fit,data):
    print "Intercept:",linear_fit.intercept_
    names = list(data.columns)
    coef = linear_fit.coef_
    for i in range(len(names)):
        print names[i],":",coef[i]

