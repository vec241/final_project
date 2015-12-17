
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

University_name1 = ""
branch_name1 = ""
University_name2= ""
branch_name2 = ""



Error_message1=None
Error_message2=None

class Window(Frame):
    """This class defines the frame of the gui and sets the title of the window"""

    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")
        self.parent = parent
        self.initUI()

    def initUI(self):

        self.parent.title("University Crimes")
        self.grid()






def gui(dataframe):


    df = dataframe['BASIC']

    root = Tk()

    def quit():
        root.destroy()
    
    
    #Title text
    Title = Label(root, text="Exploring crimes of a single university",fg="black").grid(row=0,column=0, columnspan=10,pady=10)


    #These lines print text
    prompt1 = Label(root, text="First University name :")
    prompt1.grid(pady=10,row=1,sticky=W)
    
    #Text box
    user_input1 = Entry(root,bd=3,selectforeground="yellow")
    user_input1.grid(row=1,column=1)

    prompt2 = Label(root, text="Second University name :")
    prompt2.grid(pady=10,row=2,sticky=W)
    
    #Text box
    user_input2 = Entry(root,bd=3,selectforeground="yellow")
    user_input2.grid(row=2,column=1)


    def get_branches(uni_name):
        """Returns a list of branches corresponding to a university"""
        mask=df['INSTNM']==uni_name
        subsetted_df = df[mask]
        return subsetted_df['BRANCH'].tolist()

    
    def button_press():
        """This function for what happens after GO is pressed"""

        uni_1 = str(user_input1.get())
        uni_2 = str(user_input2.get())

        lower_case_universities = df['INSTNM'].values.tolist()
        lower_case_universities = map(str.lower, lower_case_universities)

        if not(Error_message1==None):
            global Error_message1
            Error_message1 = Label(root, text="working",fg="red").grid(row=1,column=5)
            #Error_message1.grid_remove()
        if not(Error_message2==None):
            global Error_message2
            Error_message2.grid_remove()

        
        if len(uni_1)==0: #Checks if nothing is typed into the text box
            global Error_message1
            Error_message1 = Label(root, text="No input detected!",fg="red").grid(row=1,column=5)
            return None
        
        elif not(uni_1.lower() in lower_case_universities): #Checks if the university is a valid University
            global Error_message1
            Error_message1 = Label(root, text="University not found!",fg="red").grid(row=1,column=5)
            return None

        else:
            if not(Error_message1==None):
                global Error_message1
                Error_message1 = ""
                




        if len(uni_2)==0: #Checks if nothing is typed into the text box
            global Error_message2
            Error_message2 = Label(root, text="No input detected!",fg="red").grid(row=2,column=5)
            return None
        
        elif not(uni_2.lower() in lower_case_universities): #Checks if the university is a valid University
            global Error_message2
            Error_message2 = Label(root, text="University not found!",fg="red").grid(row=2,column=5)
            return None
        else:
            if not(Error_message2==None):
                Error_message2.grid_remove()

        index_of_uni = lower_case_universities.index(uni_1.lower())
        uni_1 = (df['INSTNM'].values)[index_of_uni]

        index_of_uni = lower_case_universities.index(uni_2.lower())
        uni_2 = (df['INSTNM'].values)[index_of_uni]

        set_uni1(uni_1)
        set_uni2(uni_2)

        remove_elements()

        L3 = Label(root, text="Pick a branch of {} : ".format(uni_1))
        L3.grid(pady=10,row=1,column=1)

        L4 = Label(root, text="Pick a branch of {} : ".format(uni_2))
        L4.grid(pady=10,row=2,column=1)
        
        #Text box
        choices1 = get_branches(uni_1)
        global branch1_input
        branch1_input = StringVar(root)
        branch1_input.set('None selected')
        drop1 = OptionMenu(root,branch1_input,*choices1)
        drop1.grid(row=1,column=2)

        choices2 = get_branches(uni_2)
        global branch2_input
        branch2_input = StringVar(root)
        branch2_input.set('None selected')
        drop2 = OptionMenu(root,branch2_input,*choices2)
        drop2.grid(row=2,column=2)

        #BUTTON
    	button5 = Button(text="SEARCH", command=branch_GO, fg="blue",width=10)
    	button5.grid(row=4,column =1,columnspan=5,padx=10)


    
    def branch_GO():
        """This function for what happens after SEARCH is pressed after the branch is chosen"""
        if (str(branch1_input.get()) == "None selected") or (str(branch2_input.get()) == "None selected"):
            
            return None

        set_branch1(str(branch1_input.get()))
        set_branch2(str(branch2_input.get()))


        quit()

        
    

    def remove_elements():
        prompt1.grid_remove()
        prompt2.grid_remove()
        user_input1.grid_remove()
        user_input2.grid_remove()
        go_button.grid_remove()
        if not(Error_message1==None):
            Error_message1.grid_remove()
        if not(Error_message2==None):
            Error_message2.grid_remove()


    #BUTTON
    go_button = Button(text="GO", command=button_press, fg="blue",width=5)
    go_button.grid(row=3,column =1,columnspan=4,padx=10,pady=10)
    

    
    #Quit button
    Quit_button = Button(root, text="Quit", command=quit)
    Quit_button.grid(row=6,column =1,columnspan=15,pady=10)

    app = Window(root)
    root.mainloop()




def set_uni1(Uni_name):
    global University_name1
    University_name1 = Uni_name

def set_branch1(br_name):
    global branch_name1
    branch_name1 = br_name

def get_uni1():
    return University_name1

def get_branch1():
    return branch_name1

def set_uni2(Uni_name):
    global University_name2
    University_name2 = Uni_name

def set_branch2(br_name):
    global branch_name2
    branch_name2 = br_name

def get_uni2():
    return University_name2

def get_branch2():
    return branch_name2





def start_user_interface(dataframe):
    gui(dataframe)
    

    