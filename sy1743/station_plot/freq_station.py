import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import operator
from collections import Counter

# DS-GA 1007 Final Project
# Station frequency Calculation
# Author: Sida Ye


def station_info(data, year, month):
    """
    This function will generate a dataframe with station id, station latitude, station longitude, station name and station frequency as columns.
    Input: year, month, stat_type='start' or 'end'
    """

    freqs = Counter(data['start station id'])
    location_dict = {}
    for id in data['start station id'].unique():
        if id not in location_dict.keys():
            location_dict[id] = data[data['start station id'] == id][['start station latitude', 'start station longitude','start station name']].iloc[0].values
            location_dict[id] = np.append(location_dict[id], freqs[id])
    loc_df = pd.DataFrame(location_dict).T
    loc_df = loc_df.reset_index(range(len(location_dict)))
    loc_df.columns = ['id', 'lat','long', 'name', 'freq' ]
    return loc_df

 
def high_freq_station(data, top_k):
    """
    This function will return a list of highest frequency station name.
    """
    
    sorted_freq_df = data.sort(['freq'], ascending=[False])
    topk_stations_name = np.array(sorted_freq_df[:top_k]['name'])
    return topk_stations_name
    
    