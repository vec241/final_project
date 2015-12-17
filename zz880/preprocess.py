import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

'''
This module is used to preprocess data before analysis. The module includes several functions to remove missing
or invalid values, print distribution of each covariate and check if log transformation is needed.

'''

def clean_data(initial_data):
    print "Cleaning Data ..."
    # replace inf, -inf by NAs
    data = initial_data.replace([np.inf, -np.inf], np.nan)
    # remove NAs
    data = data.dropna()
    # check if all the values are numerical
    bool = data.applymap(np.isreal)
    if (all(bool) == True):
        print "Done.\nAll the values are numerical"
    else:
        print "Done.\nThere is invalid value"
    return data


# plot_dist is used to print histograms before and after log transformation
def plot_dist(data):
    length = len(data.columns)
    for i in range(length):
        plt.clf()
        plt.hist(data[data.columns[i]])
        plt.xlabel("Value of {0}".format(data.columns[i]))
        plt.ylabel("Number of Aunctions")
        plt.title('Histogram of {0}'.format(data.columns[i]))
        plt.savefig('Histogram of {0}.pdf'.format(data.columns[i]))

# Do log transformation for skewed distributed covariates
def log_transformation(data):
    print "Doing Log Transformation ..."
    colnames = data.columns
    ncol = len(colnames)
    for i in range(1,ncol):
        data['Log {0}'.format(colnames[i])] = np.log(data[colnames[i]])
    return data



