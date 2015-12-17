__author__ = 'SeansMBP'

"""The function plotting2 takes in two parameters - 
the path of the image file, and the second choice, the user provided in GUI3"""


from Tkinter import *
from math import *
import pandas as pd
import numpy as np
import PIL
from PIL import Image, ImageTk
import matplotlib.pyplot as plt


choice2 = ""


class Window(Frame):
    """This class initializes the frame of the GUI and sets the title of the window"""

    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")

        self.parent = parent

        self.initUI()
        

    def initUI(self):

        self.parent.title("Stats of all crimes for universities belonging to {0}".format(choice2))
        self.grid()





def plotting3(path1,choice2_param):
    """Displys the two saved plots for two university and its respective branches in a GUI"""
    
    root = Tk()
    
    global choice2
    choice2 = choice2_param

    

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



    Button(root, text="DONE",width = 20, command=quit).grid(row=2,columnspan = 2,pady=10)#.pack(side = BOTTOM)

    app = Window(root)
    root.mainloop()

