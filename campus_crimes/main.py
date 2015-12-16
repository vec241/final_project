'''
Varun D N - vdn207@nyu.edu
'''

'''The main program orchestrating the different components of the project'''

import functionalities as func
import handlers
import os

if __name__ == '__main__':
	'''The main program running the software'''

	dataframe, crimes_obj = handlers.data_initialization("data/oncampuscrime101112_cleaned.csv")

	# Directory to hold the output images
	newpath = 'output' 
	if not os.path.exists(newpath):
		os.makedirs(newpath)

	try:
		func.interface(dataframe, crimes_obj)

	except (NameError, KeyError):
		print "Thanks for using!"