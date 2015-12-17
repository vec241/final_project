#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: Sean D Rosario

Description :
This script creates a GUI for "University Crimes" project,
for the NYU grad course : DS-GA-1007 Programming for Data Science


References:
ZetCode Tkinter tutorial -Jan Bodnar (www.zetcode.com)
"""



from Tkinter import *
from math import *
import pandas as pd
import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt


class Window(Frame):
    """This class initializes the frame of the GUI and sets the title of the window"""

    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")
        self.parent = parent
        self.initUI()

    def initUI(self):

        self.parent.title("University Crimes")
        self.grid()



choice_1 =""
choice_2 =""


def gui(dataframe):



    df = dataframe['BASIC']

    def quit():
        root.destroy()

    root = Tk()


    #The next 4 lines output a string
    var = StringVar()
    label = Label(root,textvariable = var,relief=RAISED,bd=0)
    var.set("Pick a category to explore the crimes by :")
    label.grid(row=0,columnspan=4,padx=10)


    

    def State():

        remove_elements()
        
        global choice_1
        choice_1="State"

        #The next 4 lines output a string
        var = StringVar()
        label = Label(root,textvariable = var,relief=RAISED,bd=0)
        var.set("Please pick a state from the drop down:")
        label.grid(row=0,columnspan=4,padx=10)

        choices = np.sort(df['State'].unique())
        drop_down_input = StringVar(root)
        drop_down_input.set('None selected')
        drop = OptionMenu(root,drop_down_input,*choices)
        drop.grid(row=1,column=1,pady=10)

        def Search():
            global choice_2
            choice_2 = str(drop_down_input.get())
            quit()

        GO_button = Button(text="SEARCH", command=Search, fg="blue")
        GO_button.grid(row=3,column =1,padx=10,pady = 20)


    
    button1 = Button(text="View crimes by STATE", command=State, fg="blue")
    button1.grid(row=1,column =1,padx=10,pady = 10)



    def Sector():
        
        remove_elements()

        global choice_1
        choice_1="Sector_desc"

        #The next 4 lines output a string
        var = StringVar()
        label = Label(root,textvariable = var,relief=RAISED,bd=0)
        var.set("Please pick a Sector from the drop down:")
        label.grid(row=0,columnspan=4,padx=10)

        choices = np.sort(df['Sector_desc'].unique())
        drop_down_input = StringVar(root)
        drop_down_input.set('None selected')
        drop = OptionMenu(root,drop_down_input,*choices)
        drop.grid(row=1,column=1,pady=10)

        def Search():
            global choice_2
            choice_2 = str(drop_down_input.get())
            quit()

        GO_button = Button(text="SEARCH", command=Search, fg="blue")
        GO_button.grid(row=3,column =1,padx=10,pady = 20)



    button2 = Button(text="View crimes by SECTOR", command=Sector, fg="blue")
    button2.grid(row=1,column =2,padx=10,pady = 10)



    def remove_elements():
        button1.grid_remove()
        button2.grid_remove()
    

    Quit_button = Button(root, text="Quit", command=quit)
    Quit_button.grid(row=6,column =1)

    app = Window(root)
    root.mainloop()


def get_choices():
    return choice_1,choice_2

def start_user_interface(dataframe):
    
    try:
        gui(dataframe)
    except:
        print "Error in GUI"
    