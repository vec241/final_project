DS-GA-1007 Project
Title: Prediction in Ebay Auctions
Author: Zhaoyin Zhu (zz880)

========================================================
This file will introduces all modules and functions used in this project and how to run this program. 

The data file EbayAuctionData.csv was collected from eBay from April 2013 to the first week of May 2013. The original dataset contains 79 attritubes like starting bid price, final price and number of bids, etc. Since the object of this project is to predict sale or not and predict final sale price, we decided to keep 9 related attributes, QuantitySold, PricePercent, StartingBidPercent, SellerClosePercent, AvgPrice, AuctionCount, AuctionSaleCount, SellerAuctionCount and AuctionMedianPrice. 

The module preprocess.py is used to preprocess data before analysis which includes 3 functions. The function clean_data removes invalid values and check if all the values are numerical. The function plot_dist is used to print histograms before and after log transformation. The function log_transformation is used to do log transformation for skewed distribution. From the figures, we can observe the log transformation is needed to make the data approximatelly normally distributed. 

The module modeling_function.py is used to split data into training and testing datasets, data preparation and fit a logistic regression model for Quantity Sold and fit a linear regression model for PricePercent. From these two models, we obtained the coefficients which can be used for prediction. 

The module evaluation_functions.py is used to evaluate the performance of logistic regreesion model and linear regression model obtained from modeling part on testing dataset. For logistic regreesion, we will report precision, recall and f-measurement. For linear regression, we will report mean square error. 

The module test.py is used to test the functions in previous files works or not. 

===========================================================
The final_project.py is used to run all the functions on the ebay auction dataset. This program will print out the process of data cleaning, generate histograms of attributes before and after log transformation, provide coeffecients of logistic and linear regression models and report the evaluation measurements on testing dataset. 

After that, the program will asks you to enter the information of the item you want to sell and gives you the probability of sale and the final sale price. You can enter "quit" to exit the program at any time.  