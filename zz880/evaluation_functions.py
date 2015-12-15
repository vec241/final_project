import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from modeling_functions import *
from preprocess import *
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score

'''
Evaluate the performance of logistic regression model on testing dataset and report precision, recall and corresponding
f-measurement
'''
def evaluate_logistic(logistic_fit, test_x, test_y):
    y_true = test_y
    y_pred = logistic_fit.predict(test_x)
    precision = precision_score(y_true,y_pred)
    recall = recall_score(y_true,y_pred)
    fmeasure = 2 * precision * recall / (precision + recall)
    print "Precision:",precision
    print "Recall:",recall
    print "F-measurement:",fmeasure

'''
Evaluate the performance of linear regression model on testing dataset and report mean square error
'''
def evaluate_linear(linear_fit, test_x, test_y):
    y_true = test_y
    y_pred = linear_fit.predict(test_x)
    mse = np.mean(pow(y_true - y_pred,2))
    print "Mean Square Error:", mse, "\n"
