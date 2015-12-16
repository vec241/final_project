__author__ = 'SeansMBP'

"""The function plotting4 takes in two parameters - 
the path of the image file, and the second choice, the user provided in GUI3"""


from Tkinter import *
from math import *
import pandas as pd
import numpy as np
import PIL
from PIL import Image, ImageTk
import matplotlib.pyplot as plt


crime1 = ""
crime2 = ""


class Window(Frame):
    """This class initializes the frame of the GUI and sets the title of the window"""

    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")

        self.parent = parent

        self.initUI()
        

    def initUI(self):

        self.parent.title("Comparison of {0} versus {1} for all universities".format(crime1,crime2))
        self.grid()





def plotting4(path1,path2,crime1_param,crime2_param):
    """Displys the two saved plots for two university and its respective branches in a GUI"""
    
    root = Tk()
    
    global crime1
    crime1 = crime1_param

    global crime2
    crime2 = crime2_param

    

    def quit():
        root.destroy()



    #
    # Displays the first image (stored in path1) after resizing it
    #

    img1 = Image.open(path1)
    img1 = img1.resize((600, 450), PIL.Image.ANTIALIAS) #Resizing the image to 600x450
    img1 = ImageTk.PhotoImage(img1)
    label1 = Label(root, image = img1)
    label1.image = img1 # keep a reference of the image
    label1.grid(row = 1,column =0,pady=10,padx=20)

    #
    # Displays the second image (stored in path2) after resizing it
    #
    img2 = Image.open(path2)
    img2 = img2.resize((600, 450), PIL.Image.ANTIALIAS) #Resizing the image to 600x450
    img2 = ImageTk.PhotoImage(img2)
    label2 = Label(root, image = img2)
    label2.image = img2 # keep a reference of the image
    label2.grid(row=1,column=1,pady=10,padx=20)



    Button(root, text="DONE",width = 20, command=quit).grid(row=2,columnspan = 2,pady=10)#.pack(side = BOTTOM)

    app = Window(root)
    root.mainloop()