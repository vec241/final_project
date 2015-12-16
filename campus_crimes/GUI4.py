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

crime_1 = ""
crime_2 = ""


class Window(Frame):
    """This class defines the frame of the gui and sets the title of the window"""

    def __init__(self, parent):
        Frame.__init__(self, parent, background="grey")
        self.parent = parent
        self.initUI()

    def initUI(self):

        self.parent.title("GUI 4")
        self.grid()






def gui():

    global root
    root = Tk()

    def quit():
        root.destroy()

    #The next 4 lines output a string
    var1 = StringVar()
    label1 = Label(root,textvariable = var1,relief=RAISED,bd=0)
    var1.set("Pick two categories of crimes")
    label1.grid(row=1,column =1,columnspan=4,pady =10)


    crime_full_names = {"MURD":"Murder", "NEG_M":"Negligent Manslaughter", "FORCIB":"Forcible Sex Offense", "NONFOR":"Non Forcible Sex Offense", "ROBBE":"Robbery", "AGG_A":"Aggravated Assault", "BURGLA":"Burglary", "VEHIC":"Motor Vehicle Theft", "ARSON":"Arson"}
    crime_full_names = dict (zip(crime_full_names.values(),crime_full_names.keys()))


    choices = crime_full_names.keys()

    drop_down_input1 = StringVar(root)
    drop_down_input1.set('None selected')
    drop1 = OptionMenu(root,drop_down_input1,*choices)
    drop1.grid(row=2,column=1,pady=10,padx=10)

    drop_down_input2 = StringVar(root)
    drop_down_input2.set('None selected')
    drop2 = OptionMenu(root,drop_down_input2,*choices)
    drop2.grid(row=2,column=2,pady=10,padx=10)
    

    
    def go():
        """This function is for the GO button"""
        global crime_1
        crime_1 = crime_full_names[str(drop_down_input1.get())]
        global crime_2
        crime_2 = crime_full_names[str(drop_down_input2.get())]

        if crime_1 == crime_2:
            
            #The next 4 lines output a string
            var2 = StringVar()
            label2= Label(root,textvariable = var2,relief=RAISED, bd =0)
            var2.set("ERROR: Please choose different crimes!")
            label2.grid(row=4,column =1,columnspan=4,pady =10)

        
        else:
            quit()



        
    
    #BUTTON
    GO_button = Button(text="GO", command=go, fg="blue")
    GO_button.grid(row=3,column =1,columnspan=3,pady=10,padx=10)

    
    Quit_button = Button(root, text="Quit", command=quit)
    Quit_button.grid(row=5,column =2,pady=20)

    app = Window(root)
    root.mainloop()






def get_crimes():
    return crime_1,crime_2





def start_user_interface():
    try:
        gui()
    except:
        print "Error in GUI"

#if __name__ == '__main__':
    #gui()
    #print get_crimes()
    