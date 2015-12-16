__author__ = 'SeansMBP'


from Tkinter import *
from math import *
import pandas as pd
import numpy as np
import PIL
from PIL import Image, ImageTk
import matplotlib.pyplot as plt


uni_name = ""
branch_name = ""

class Window(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")

        self.parent = parent

        self.initUI()
        

    def initUI(self):

        self.parent.title("Crime details of {0}".format(uni_name))
        self.grid()





def plotting1(path1,path2,uni_name_param,branch_name_param):
    
    root = Tk()
    
    global uni_name
    uni_name = uni_name_param

    global branch_name
    branch_name = branch_name_param

    

    def quit():
        root.destroy()

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

    Button(root, text="DONE",width = 20, command=quit).grid(row=4,columnspan = 2,pady=10)#.pack(side = BOTTOM)

    app = Window(root)
    root.mainloop()


#if __name__ == '__main__':
    #plotting1("plot1.jpg","plot2.jpg","NYU")