'''
This program is on loading and cleaning the dataset used in the analysis.
'''

import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    df=pd.read_csv('311_Service_Requests_from_2010_to_Present.csv',sep=',',low_memory=False,nrows=50000)
    return df
    
def clean_data(data):
    #extract useful columns
    create_data=data['Created Date']
    city=data['City']
    complaint_type=data['Complaint Type']
    zip_code=data['Incident Zip']
    facility_status=data['Status']
    location_type=data['Location Type']
    df_new=pd.concat([create_data,city,complaint_type,zip_code,facility_status],axis=1,join='outer')
    #rename columns
    df_new.columns=['created_date','city','complaint_type','incident_zip','facility_status']
    df_new.dropna(how='any',inplace=True)
    df_new['city']=map(lambda x: x.upper(),df_new['city'])
    #print df_new
    df_new['date']=pd.to_datetime(df_new['created_date'])
    df_new['year']=df_new['date'].apply(lambda x: x.year)
    df_new['hour']=df_new['date'].apply(lambda x: x.hour)
    df_new.to_csv('data_new.txt')
    df2=pd.concat([city,complaint_type,location_type],axis=1,join='outer') #df2 is for location type
    df2.columns=['city','complaint_type','location_type']
    df2.dropna(how='any',inplace=True)
    df2.to_csv('location_type_for_all_city.csv')
    return df_new,df2

'''
data=load_data()
data,location_type=clean_data(data)
print "done" 
'''



def reload_data():
    data=pd.read_csv('sample_data.csv')
    location_type_data=pd.read_csv('location_type_for_all_city.csv',index_col=0)
    return data, location_type_data

