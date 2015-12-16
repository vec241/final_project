__author__ = 'SeansMBP'


#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: Sean D Rosario

Description :
This script creates a GUI for "University Crimes" project,
for the NYU grad course : DS-GA-1007 Programming for Data Science


References:
ZetCode Tkinter tutorial
Author: Jan Bodnar (www.zetcode.com)
"""



from Tkinter import *
from math import *
import pandas as pd
import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt



global result
root = None

class Window(Frame):
	"""This class initializes the frame of the GUI and sets the title of the window"""
	def __init__(self, parent):
		Frame.__init__(self, parent, background="white")
		self.parent = parent
		self.initUI()
		
   

	def initUI(self):
		self.parent.title("University Crimes")
		self.grid()






def initial_gui():
	"""This function launches the first GUI which presents the user with 4 buttons.
		The button set a value of result which indicates which is the next GUI to be launched"""


	global root
	root = Tk()
	result = 0

	def quit():
		root.quit()


	#The next 4 lines output a string
	var = StringVar()
	label = Label(root,textvariable = var,relief=RAISED,bd=0)
	var.set("EXPLORE CRIMES IN AMERICAN UNIVERSITIES")
	label.grid(row=0,columnspan=4,pady = 10)


	#The next 4 lines output a string
	var = StringVar()
	label = Label(root,textvariable = var,relief=RAISED,bd=0)
	var.set("Click on any one of the following 4 options ")
	label.grid(row=2,columnspan=4,pady = 10)


	
	#BUTTON
	button1 = Button(text="Single University", command=option1, fg="blue")
	button1.grid(row=3,column=1,pady = 10)

	button2 = Button(text="Compare two universities", command=option2, fg="blue")
	button2.grid(row=4,column=1,pady = 10)

	button3 = Button(text="View crimes by category", command=option3, fg="blue")
	button3.grid(row=5,column=1,pady = 10)

	button4 = Button(text="Compare two crimes", command=option4, fg="blue")
	button4.grid(row=6,column=1,pady = 10)

	quit_button =Button(text="QUIT", command=quit, fg="black")
	quit_button.grid(row=7,column=1,pady = 20)

	app = Window(root)
	root.mainloop()



def option1():
	'''Sets the value of result to 1 and quits the GUI'''
	global result
	result =1
	global root
	root.destroy()


def option2():
	'''Sets the value of result to 2 and quits the GUI'''
	global result
	result =2
	global root
	root.destroy()


def option3():
	'''Sets the value of result to 3 and quits the GUI'''
	global result
	result =3
	global root
	root.destroy()

def option4():
	'''Sets the value of result to 4 and quits the GUI'''
	global result
	result =4
	global root
	root.destroy()


def get_result():
	return result

	