'''
Fall 2015 DS-GA 1007 Programming for Data Science 
Final Project
Authors: Menghan Yuan, Xu Xu

This is the main program of Fina Project.
The project is to analyze complaints in NYC according to the user's input, the zipcode.
The results of the project can be used to decide whether the district is good for live or not.
Firstly an overall analysis of the major boroughs that shows the total number of all kinds of complaints from 2010-2015.
If the user input is a valid 5-digit zipcode of NYC, firstly the top 5 kinds of complaints will be showed as a histogram in different years.
The historgram is used to show the number and trend of top 5 kinds of complaints from 2010-2015.
After Closing the histogram window, a pie chart with top 10 kinds of complaints will show the top 10 complaints that 
happened most frequently in last 5 years.
After the pie chart, a line chart shows the total number of reported complaints along with the time in hours.
With all kinds of complaints displaying, the user will be request to enter a complaint listed above.
If the user finish look through the histogram on locations of complaints happening or want to ignore it, input 'continue'.
The pie chart is to show the status of all reported complaints in the given city according to the zipcode.
Input 'quit' to finish the program.
'''
from load_and_clean_data import *
from graph_functions import *
from zip_code_belonging_city import *
import sys

print "*********************************************************************************"
print "Welcome to NYC Complaints!"
print "From here you can find the analysis of any complaints happened in your target "
print "district in NY so that you can make decision whether to live here or not :)"
print "Please follow the instructions to start your journey!"
print "*********************************************************************************"


data,location_type_data=reload_data()
zip_code_dictionary=create_zip_code_dict(data)
print 'Generating the Graph of Total Complaints for Six Years in NYC ...'
print 'Note:when a figure window pop up,you need to close the figure window before continuing the program, same for later'
all_area_all_year_by_city(data) #generate the total number of each borough in NYC from 2010 to 2015
print 'Brooklyn Has the Most Complaints in Last 6 year, While Corona Has the Lease!'
print '-----------------------------------------------------------------------------------'
try:
    quit_flag = False
    while not quit_flag:
        print 'If You Want To Quit, Please Input "quit"!'
        zip_code=raw_input('Please Input the Zipcode (eg.10001, 11201) of the District You Are Interested In:\n')
        
        if zip_code in ('quit', 'finish'): #user wants to quit the analysis
            quit_flag = True
            sys.exit()
        elif zip_code.isdigit() == False: #the user do not input in numbers
            print "Please Input in NUMBERS!"
        elif zip_code.isdigit() == True: #the user input in numbers
            print 'YES! Your Input is NUMBER!'
            try:
                length = int(len(str(zip_code))) #to judge whether the input is a number is 5-digit
                if length == 5:
                    print 'Zipcode Format Match!'
                    city=show_belonging(zip_code,zip_code_dictionary)
                    print 'The Zipcode You Entered Belongs To: ',city
                    #print data.head()
                    print 'Generating Overall analysis in {:s} ...'.format(city)
                    city_data=get_sorted_complaint_data_by_city(data,city)
                    specific_city_all_year_first_5_complain(city_data,city) #draw bar chart
                    specific_city_all_year_piechart(city_data,city)  #draw pie chart
                    print 'Generating The Line Chart of The Number of Complaints in HOURS'
                    time_trend_line(data,city) #draw the line chart
                    
                    
                    complaintype_list=create_complaint_type_dict(data)
                    print '-------------------------------------------------------------------------------------------'
                    print complaintype_list #show all the complaint type in the given district
                    while not quit_flag:
                        print 'If You Do Not Want To See the Distribution of A Given Complaint Type and Want To See the Status of Complaints, Please Input "Continue" '
                        complaint_type = raw_input('Please Enter the Complaint Type Showed Above to Check (Pay Attention to the Case Sensitivity and FORMAT! eg.Noise - Commercial): \n')
                        
                        #let user input the complaint type they insterested in 
                        if complaint_type in ('quit','finish'):
                            quit_flag = True
                            sys.exit() #user input quit, then the program ends
                        elif complaint_type in complaintype_list: #when users input the exact complaint type showed above 
                            print 'Show the Most Popular Complaint Locations:'
                            #show the histogram of the different locations
                            plot_location_type_for_particular_complaint_in_city(location_type_data,city,complaint_type)
                        elif complaint_type in ('continue', 'go on'): #user want to see the status of complaints, the program will show the pie chart
                            print 'The Analysis of the Complaint Status in the District is Continuing'
                            break
                            
                        else:
                            print 'Please Input the Complaint Type In The Format Showed Above!'
                            print '--------------------------------------------------------------------'
                    print 'Show the Facility Status in {}'.format(city)
                    frequency=get_data_for_piechart(data,zip_code)
                    status_piechart(frequency)
                    print 'Conguatulations! Done with the analysis of given district in {}'.format(city)
                    print '**********************************************************************'
                    
                
                else:
                    print 'But Please Input a 5-Digit Zipcode!'
            except ValueError:
                print 'Please Input a 5-Digital Zipcode!'
except KeyboardInterrupt:
    print 'Please Run the Program Agian!'
except Exception:
    print 'Exception: The Complaint Type Cannot Generate Chart. Please Run the Program Again!'

