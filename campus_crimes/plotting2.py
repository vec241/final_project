__author__ = 'SeansMBP'

"""This module contains the plotting2 function, 
which takes in the paths of the images with the names of universities 
and branches and runs an interactive GUI which displays the output plots  
based on the inputs in GUI2"""


from Tkinter import *
from math import *
import pandas as pd
import numpy as np
import PIL
from PIL import Image, ImageTk
import matplotlib.pyplot as plt


uni_name1 = ""
branch_name1 = ""

uni_name2 = ""
branch_name2 = ""

class Window(Frame):
    """This class initializes the frame of the GUI and sets the title of the window"""

    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")

        self.parent = parent

        self.initUI()
        

    def initUI(self):

        self.parent.title("Comparison of crimes between {0} - {1} and {2} - {3}".format(uni_name1,branch_name1,uni_name2,branch_name2))
        self.grid()





def plotting2(path1,path2,path3,path4,uni_name1_param,branch_name1_param,uni_name2_param,branch_name2_param):
    """Displys the two saved plots for two university and its respective branches in a GUI"""
    
    root = Tk()
    
    global uni_name1
    uni_name1 = uni_name1_param

    global branch_name1
    branch_name1 = branch_name1_param

    global uni_name2
    uni_name2 = uni_name2_param

    global branch_name2
    branch_name2 = branch_name2_param

    

    def quit():
        """Quits the GUI"""
        root.destroy()



    #
    # Displays the first image (stored in path1) after resizing it
    #

    img1 = Image.open(path1)
    img1 = img1.resize((550, 400), PIL.Image.ANTIALIAS) #Resizing the image to 600x450
    img1 = ImageTk.PhotoImage(img1)
    label1 = Label(root, image = img1)
    label1.image = img1 # keep a reference of the image
    label1.grid(row = 1,column =1,pady=10,padx=20)


    #
    # Displays the second image (stored in path2) after resizing it
    #
    img2 = Image.open(path2)
    img2 = img2.resize((550, 400), PIL.Image.ANTIALIAS) #Resizing the image to 600x450
    img2 = ImageTk.PhotoImage(img2)
    label2 = Label(root, image = img2)
    label2.image = img2 # keep a reference of the image
    label2.grid(row=1,column=2,pady=10,padx=20)

    def next_result():
        """Removes the first two plots and replaces them with the next two plots"""

        label1.grid_remove()
        label2.grid_remove()
        next_result_button.grid_remove()

        #
        # Displays the third image (stored in path3) after resizing it
        #

        img3 = Image.open(path3)
        img3 = img3.resize((550, 400), PIL.Image.ANTIALIAS) #Resizing the image to 600x450
        img3 = ImageTk.PhotoImage(img3)
        label3 = Label(root, image = img3)
        label3.image = img3 # keep a reference of the image
        label3.grid(row = 1,column =1,pady=10,padx=20)
        
        
        #
        # Displays the fourth image (stored in path4) after resizing it
        #
        img4 = Image.open(path4)
        img4 = img4.resize((550, 400), PIL.Image.ANTIALIAS) #Resizing the image to 600x450
        img4 = ImageTk.PhotoImage(img4)
        label4 = Label(root, image = img4)
        label4.image = img4 # keep a reference of the image
        label4.grid(row=1,column=2,pady=10,padx=20)

    
    next_result_button = Button(root, text="VIEW NEXT RESULT >",width = 20, command=next_result)
    next_result_button.grid(row=2,column =1,columnspan = 2,pady=10)#.pack(side = BOTTOM)
    Button(root, text="DONE",width = 20, command=quit).grid(row=3,column =1,columnspan = 2,pady=10)#.pack(side = BOTTOM)
    
    app = Window(root)
    root.mainloop()


#if __name__ == '__main__':
    #plotting2("plot1.jpg","plot2.jpg","plot1.jpg","plot2.jpg","NYU","NYU","NYU","NYU")