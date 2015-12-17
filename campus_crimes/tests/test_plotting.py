''' check that code runs well '''
#author: Michael Higgins
#netid: mch529

#https://docs.python.org/2/library/unittest.html

import custom_exceptions as cexcep
from unittest import TestCase
import plots
import plottingParameters
import pandas as pd
import numpy as np

class Test(TestCase):
	
	
	def setUp(self):
		self.p= plottingParameters.pltParam()
		self.clrs =self.p.getColors(5)
		self.bigColors= self.p.getColors(100)
		
		# variables for testing alternating dictionary		
		self.validInputAlternating1={"a":3,"b":2,"c":5}
		self.validInputAlternating2={"a":2,"b":3,"c":5}
		self.validInputAlternating3={"a":2,"b":3,"c":5,"d":-3}
		self.validInputAlternating4={"d":5,"c":4,"b":3,"a":-2}
		self.invalidInputAlternating1= "word,yo"
		self.invalidInputAlternating2= -3.14
		
		#variables for checking fontSizeMaker
		self.validSmallTick =3
		self.validBigTick =100
		
	
	
	def test_getColors(self):
		''' check that colors is running correctly '''
	 	
		self.assertEquals(len(self.clrs), 5)   #check colors is of correct length
		self.assertEquals(type(self.clrs),list) #check type
		self.assertEquals(type(self.clrs[0]),tuple) #type inside list
		self.assertRaises( ZeroDivisionError,  self.p.getColors, 0  ) # cant have 0 input
		self.assertEquals( len(set(self.bigColors)), len(self.bigColors) )  #check that they are unique colors
		

	
	def test_alternatingDictionary(self):
		''' check that return list is correct and input is correct '''
		self.assertEquals(self.p.alternatingDictionary(self.validInputAlternating1 ),   ["b","c","a"]) 
		self.assertEquals(self.p.alternatingDictionary(self.validInputAlternating2 ),   ["a","c","b"]) 
		self.assertEquals(self.p.alternatingDictionary(self.validInputAlternating3 ),   ['d', 'c', 'a', 'b']) 
		self.assertEquals(self.p.alternatingDictionary(self.validInputAlternating4 ),   ['a', 'd', 'b', 'c'])
		
					
	def test_getTickFontSize(self):
		'''check getTickFontSize for correct inputs and outputs'''
		#check big and small texts
		self.assertEquals(self.p.getTickFontSize(self.validSmallTick),  20) 
		self.assertEquals(self.p.getTickFontSize(self.validBigTick),  4) 


	
