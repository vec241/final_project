'''
author: Michael Higgins -mch529
Class that generates all graphs

'''

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from matplotlib.offsetbox import AnchoredText
import handlers
import college
import crimes
import matplotlib.patches as mpatches
import random
from scipy.interpolate import interp1d
import plottingParameters as p
import random

import custom_exceptions as cexcep
from collections import OrderedDict


class Answers:
	'''Takes data and plots a relavent visualization based on that data'''
	
	
	
	def __init__(self, crimeObj, collegeObj, pltparam, answer1,answer2,answer3):
		'''Constructor'''
		self.answer1=answer1   #currently is a dictionary with Series as value
		self.answer2=answer2   #currently is a dictionary with array for value
		self.answer3=answer3
		self.crimes_list = crimeObj.get_crimes_list_short()
		self.crimeNames= crimeObj.get_crimes_list_long()
		self.crimeObj=crimeObj
		self.pltparam = pltparam
		self.collegeObj = collegeObj

	def visualize_answer1(self):
		'''
		input is a tuple, the first entry is a dictionary with the crime as a key and the rate as a value
		'''
		plt.close("all")
		ax = plt.subplot(111)		
		x = np.array(range(1, len(self.crimes_list) + 1)) #
		
		#seperate data by year instead of crime
		y_10=[]
		y_11=[]
		y_12=[]
	    
		for crime in self.crimes_list: 
			y_10.append(self.answer1[crime][0]*10000)   #multiply by 10000 y-axis is per 10000
			y_11.append(self.answer1[crime][1]*10000)
			y_12.append(self.answer1[crime][2]*10000)

		
		#bar for each year
		rect1 = ax.bar( x - self.pltparam.width, y_10 , width = self.pltparam.width, color='r', align='center')
		rect2 = ax.bar(x, y_11, width = self.pltparam.width, color='g', align='center')
		rect3 = ax.bar(x + self.pltparam.width, y_12, width = self.pltparam.width, color='b', align='center')
		
		#set ticks and rotate text
		plt.xticks([ a + self.pltparam.width/2 for a in  x],[name for name in self.crimeNames], rotation= 30, ha='right') 
		
		
		ax.set_xlabel('Particular Crime by Year ', fontsize=self.pltparam.fontsize)
		ax.set_ylabel('Crime Rate (per 10,000 students)', fontsize=self.pltparam.fontsize)
		ax.set_title(str(self.collegeObj.get_college_name()[0] )+ " Crime By Year ",fontsize=20)
		ax.autoscale(tight=True)
 
		#add 	padding
		plt.subplots_adjust(left=0.15,top=0.85)
		#legends
		r_patch = mpatches.Patch(color='red', label='2010')
		g_patch = mpatches.Patch(color='g', label='2011')
		b_patch = mpatches.Patch(color='b', label='2012')
		ax.legend([r_patch,g_patch,b_patch],['2010','2011','2012'])

		#adjust limits of yaxis to make room for annointed text
		maxData=max(y_10+y_11+y_12)
		plt.ylim(0,maxData * 1.15)
		
		for rects in [rect1,rect2,rect3]:   
			# attach some text labels
			for rect in rects:
				height = rect.get_height()
				if height !=0:  # if no crime don't show the crime rate
					ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
						    '%.1f' % height,
						    ha='center', va='bottom')
		plt.tight_layout()
		plotName =str("output/" + self.collegeObj.get_college_name()[0]) + "_answer1" + ".png"
		plt.savefig(plotName) 
		return plotName


	def simpleBarChart(self,data, specificCategory):
		'''
		input: dictionary with keys as crimes and series with state / sector as index, vals are rate
		Note: aesthetically better if series is sorted 
		output: barChart 
		'''

		plt.close("all")

		# wrangle data to get info of interest
		data = self.pltparam.subsetDictionary(data , specificCategory)
			
		data.sort()
		
		maskForEmptyBars = data <.00001
		data[ maskForEmptyBars]=.00001  #bars dont show up if values are 0 
		
		heights = (data * 10000).values  
		labels = list(data.index)
		numBars = len(labels)
		
		ax = plt.subplot(111)
		x = range(numBars)
		rects = ax.bar(x, heights, width = self.pltparam.width, align='center')
		
		#set ticks and rotate text
		try:
			plt.xticks([ a + self.pltparam.width/2 for a in  x],[self.crimeObj.get_full_name(name) for name in labels], rotation= 45, ha='right', fontsize = self.pltparam.getTickFontSize(numBars) ) 
		except cexcep.WrongFormat as er:
			print er
	
		ax.set_xlabel('Particular Crime by Year ', fontsize=self.pltparam.fontsize)
		ax.set_ylabel('Crime Rate (per 10,000 students)', fontsize=15)
		ax.set_title(" Crime by " + str(specificCategory) , fontsize=15)
		ax.autoscale(tight=True)

		#add padding
		#plt.subplots_adjust(left=0.15,top=0.85)
		plt.tight_layout()
		plotName = "output/" + str(specificCategory)+ "_answer1" + ".png"
		plt.savefig(plotName) 
		return plotName




	def visualize_answer4(self, crime1 , crime2, plot_category):
		'''
		Inputs are short names for two crimes
		saves scatterplot of two crimes circles are states and returns name of image
		'''
		plt.close("all")

		ax = plt.subplot(111)
		
		labels = list(self.answer3[crime1].index.values)
		numPoints= len( labels)
		
		#fontSizeFunction = interp1d([5,75],[20,5])  #pick mapping for size of font
		#fontsize = 15		
		#fontsize= float( fontSizeFunction(numPoints) )
		
		dataX = list(self.answer3[crime1].values*10000)
		dataY = list(self.answer3[crime2].values*10000)
		
		plt.scatter(dataX,dataY)
		
		ax.set_xlabel(self.crimeObj.get_full_name(crime1) , fontsize=self.pltparam.fontsize)
		ax.set_ylabel(self.crimeObj.get_full_name(crime2) , fontsize=self.pltparam.fontsize)
		ax.set_title(crime1 + " vs. " + crime2 + " by "+ plot_category, fontsize= 20 )
		ax.autoscale(tight=True)
		
		#labels
		#http://stackoverflow.com/questions/5147112/matplotlib-how-to-put-individual-tags-for-a-scatter-plot
		zippedData = zip(labels, dataX, dataY)
		sortedByDistance = sorted(zippedData, key=lambda tup: tup[1]**2 +tup[2]**2 ,reverse=True)
		
		#cases for if separated by state or sector
		if numPoints>12:	#by state	
			numPointsToLabel =12
		numPointsToLabel = numPoints   #by sector
		
		for label, x, y in sortedByDistance[:numPointsToLabel]:
			plt.annotate(label,xy = (x, y),xytext = (-5,5),textcoords = 'offset points',
bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),  )
		
		#add padding
		plt.subplots_adjust(left=0.15,top=0.85)
		plt.tight_layout()
		
		# saving image and returning string of file name
		plotName = "output/" + "scatter_"+crime1 + "_by_" + crime2 + "_" + plot_category + ".jpg"
		plt.savefig(plotName)
		return plotName

	def pieChart(self,data):
		'''
		input: dictionary, vals must be nonnegative
		output: pieChart with alternating sizes of pieslices (to avoid overlapping of labels) 
		'''

		plt.close("all")

		plt.figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')

		#ordering dictionary and then alternating big and small values
		keys= data.keys()
		emptyKeys = [key for key in keys if data[key]<10**(-7) ]  #get names of keys that didnt occur
		nonEmptyKeys = list(set(keys) - set(emptyKeys))   #clever way to take dif of two sets
		numPieces = len(nonEmptyKeys)

		sizes = [ data[key] for key in nonEmptyKeys ]  #remove empty crimes from values

		#put back in dictionary form so that it will be accepted by alternatingDictionary
		try:
			labels = self.pltparam.alternatingDictionary( dict(zip(nonEmptyKeys, sizes)) )	
		except cexcep.WrongFormat as er:
			print er
		

		sizes = [ data[key] for key in labels ]	#reset sizes according to new reordering of labels
		
		 #if the sum of the sizes is not one we need to normalize
		sizes = [ size/sum(sizes) for size in sizes]  #by altering our size list so sum of entries is 1
		
		try:  
			colors = self.pltparam.getColors(numPieces)  #get appropriate number of evenly spaced colors
		except cexcep.WrongFormat as er:
			print er
		
		
		indexesToExplode=[0]
		explode = [.03 for a in range(numPieces) ] # set default for slices to be slightly separated
		
		if numPieces >0:		
			for index in indexesToExplode:
				explode[index]=.2
			
		longFormatCrimes=[self.crimeObj.get_full_name(crime) for crime in labels ]

		plt.pie(sizes, explode=explode, labels=longFormatCrimes, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
		
		collegeName = str(self.collegeObj.get_college_name()[0])

		plt.title("Crime in " + collegeName , fontsize=20, y=1.08 )
		plt.subplots_adjust(top=0.85)  #to fit the title without overlap
		
		plt.axis('equal') # Set aspect ratio to be equal so that pie is drawn as a circle.
		plotName = "output/" + "Pie_Crime_in_" + collegeName + ".png"
		plt.savefig(plotName)

		return plotName
