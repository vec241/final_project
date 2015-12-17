import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from modeling_functions import *
from preprocess import *
from evaluation_functions import *
from predict_functions import *

def main():
    # Load data and remove NAs
    data = pd.read_csv("EbayAuctionData.csv")
    # Check if all the values are numerical
    cleaned_data = clean_data(data)
    # Do log transformation
    log_data = log_transformation(cleaned_data)
    # Clean data again
    cleaned_log_data = clean_data(log_data)
    #plot_dist(cleaned_log_data) # print histograms to check if log transformation is needed.
    '''
     From the histogram, we can observe that the distributions of all the covariates but Quantity Sold are positive
     skewed which indicates log transformation is required. And we can see that after log transformation, the covariates
     are normally distributed.
    '''

    # Split data into training and testing sets
    train,test = split_data(cleaned_log_data)

    # Prepare data for logistic regression to predict if an item will be sold or not
    train_logistic_x, train_logistic_y = logistic_prepare(train)
    # fit logistic regression model
    logistic_fit = logistic_model(train_logistic_x,train_logistic_y)
    # print coefficients of logistic regression
    print "\nCoefficients of logistic regression model"
    coef_logistic(logistic_fit,train_logistic_x)

    # Prepare data for linear regression to predict final sale price of an item
    train_linear_x, train_linear_y = linear_prepare(train)
    # fit logistic regression model
    linear_fit = linear_model(train_linear_x,train_linear_y)
    # print coefficients of logistic regression
    print "\nCoefficients of linear regression model"
    coef_linear(linear_fit,train_linear_x)

    # Prepare data for evaluating logistic model
    test_logistic_x, test_logistic_y = logistic_prepare(test)
    # Evaluate logistic regression model on testing set
    print "\nPerformance of logistic model"
    evaluate_logistic(logistic_fit,test_logistic_x,test_logistic_y)

    # Prepare data for evaluating linear model
    test_linear_x, test_linear_y = linear_prepare(test)
    # Evaluate logistic regression model on testing set
    print "\nPerformance of linear model"
    evaluate_linear(linear_fit,test_linear_x,test_linear_y)


    # Predict the probability an item with certain covariates will be sold
    predict_data = prediction_input()
    predict_logistic(predict_data,logistic_fit)
    predict_linear(predict_data,linear_fit)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print ("Accidently stopped by keyboard interrupt")
    except ValueError:
        print("Accidently stopped by invalid value")
    except TypeError:
        print("Accidently stopped by invalid types")
