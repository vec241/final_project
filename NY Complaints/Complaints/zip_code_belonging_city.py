'''
This program is to define which borough the input zipcode belongs to. 
And make the complaint type into a dictionary.
'''
import pandas as pd

def create_zip_code_dict(data):
    '''
    arguement:
    '''
    city_list=data['city'].unique().tolist()
    #print len(city_list)
    zip_code_dictionary={}
    for city in city_list:
        filtered_data=data[data['city']==city]
        #print filtered_data['incident_zip']
        zip_code_list=filtered_data['incident_zip'].tolist()
        zip_code_list=list(set(zip_code_list))
        zip_code_dictionary[city]=zip_code_list
    return zip_code_dictionary

def create_complaint_type_dict(data):
    complaintype_list = data['complain_type'].unique().tolist()
    return complaintype_list


def show_belonging(zip_code,dictionary): # map the borough of the input zipcode
    city=None
    for k in dictionary.keys():
        if zip_code in dictionary[k]:
            city=k
            break
    return city
