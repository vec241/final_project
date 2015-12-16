"""
Author: Sean D'Rosario

This module is run once, to clean the data and save the cleaned up data as a new csv file


"""

from math import *
import pandas as pd
import numpy as np



def remove_bad_states(input_df):
	'Removes territories that are not states'
	mask = input_df['State'].isin(['PR', 'GU', 'PW', 'VI', 'MH', 'AS', 'MP', 'FM'])
	clean_df = input_df[~mask]
	return clean_df

def remove_branches_outside_USA(input_df):
	'Filters ou branches outside USA, by checking if the corresponding State value is a missing value'
	clean_df = input_df.dropna(subset = ['State'])
	return clean_df

def remove_unwanted_sector(input_df):
	'Removes unwanted sector - Administrative sector'
	clean_df = input_df[~(input_df['Sector_desc']=='Administrative Unit Only')]
	return clean_df

def remove_unwanted_columns(input_df):
	'Removes unwanted columns - namely: "City", "Address", "ZIP", "sector_cd"'
	clean_df = input_df.drop(["City", "Address", "ZIP", "sector_cd"],axis =1)
	return clean_df

def remove_no_crime_entries(input_df):
	'Removes all the univeristy branches that have no or barely any crime (unreported stats)'
	sum_of_crimes = (input_df.ix[:,7:34]).sum(axis=1)
	clean_df = input_df[sum_of_crimes>5]
	return clean_df


if __name__ == "__main__":
	df = pd.read_excel('data/oncampuscrime101112.xls')
	df = remove_bad_states(df)
	df = remove_branches_outside_USA(df)
	df = remove_unwanted_sector(df)
	df = remove_unwanted_columns(df)
	df = remove_no_crime_entries(df)
	df.to_csv("data/oncampuscrime101112_cleaned.csv", sep=',', encoding='utf-8')
	


